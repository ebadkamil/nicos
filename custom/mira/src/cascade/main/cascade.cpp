﻿// *****************************************************************************
// NICOS, the Networked Instrument Control System of the FRM-II
// Copyright (c) 2009-2013 by the NICOS contributors (see AUTHORS)
//
// This program is free software; you can redistribute it and/or modify it under
// the terms of the GNU General Public License as published by the Free Software
// Foundation; either version 2 of the License, or (at your option) any later
// version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
// details.
//
// You should have received a copy of the GNU General Public License along with
// this program; if not, write to the Free Software Foundation, Inc.,
// 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//
// Module authors:
//   Tobias Weber <tweber@frm2.tum.de>
//
// *****************************************************************************
/*
 * Cascade Viewer Main Window
 * (Plotter initially based on "spectrogram" qwt sample code)
 */

// Werden Daten vom Server zlib-komprimiert gesendet?
// Dies hat nichts mit der "Pseudokompression" zu tun!
//#define DATA_COMPRESSED

#include <iostream>
#include <stdlib.h>
#include <limits>
#include <string.h>
#include <exception>

#include <QtGui/QApplication>
#include <QtGui/QMainWindow>
#include <QtGui/QToolBar>
#include <QtGui/QToolButton>
#include <QtGui/QPrinter>
#include <QtGui/QPrintDialog>
#include <QtGui/QPen>
#include <QtCore/QVariant>
#include <QtCore/QTimer>
#include <QtGui/QGridLayout>
#include <QtGui/QMenu>
#include <QtGui/QMenuBar>
#include <QtGui/QStatusBar>
#include <QtGui/QGroupBox>
#include <QtGui/QFileDialog>
#include <QtGui/QSlider>
#include <QtGui/QLabel>
#include <QtGui/QPainter>
#include <QtGui/QDialog>
#include <QtCore/QLine>
#include <QtGui/QMessageBox>
#include <QtCore/QSettings>

#include "../config/globals.h"
#include "../loader/tofloader.h"
#include "../plot/tofdata.h"
#include "../plot/bins.h"
#include "../config/config.h"
#include "../client/client.h"
#include "../auxiliary/parse.h"
#include "../main/cascadewidget.h"
#include "../auxiliary/logger.h"
#include "../auxiliary/helper.h"
#include "../auxiliary/gc.h"

#include "../plot/ErrorBarPlotCurve.h"
#include "../plot/histogram_item.h"
#include "../dialogs/cascadedialogs.h"

#ifdef DATA_COMPRESSED
	#include "decompress.h"
#endif


int main(int, char **);

////////////////////////////// Haupt-Fenster ///////////////////////////////////
class MainWindow : public QMainWindow
{
  Q_OBJECT
	private:
		friend int main(int, char **);

		// Anzahl der Bins für Kalibrationsdialog
		static int NUM_BINS;
		static int SERVER_STATUS_POLL_TIME;
		static int AUTOFETCH_POLL_TIME;

	protected:
		CascadeWidget m_cascadewidget;

		TcpClient m_client;
		QTimer m_statustimer, m_autofetchtimer;

		std::string m_strTitle;
		QLabel *labelZeitkanal, *labelFolie;

		QToolButton *btnLog, *btnAutoFetch;

		QSlider *sliderFolien, *sliderZeitkanaele;

		QStatusBar *statusbar;
		QLabel *pStatusMsg, *pStatusExtCount;

		QAction *actionViewsOverview, *actionViewsSlides,
				*actionViewsPhases, *actionViewsContrasts;

		void Unload()
		{
			//m_cascadewidget.SetMode(MODE_SLIDES);
			m_cascadewidget.Unload();
		}

		bool CheckConnected()
		{
			if(!m_client.isconnected())
			{
				QMessageBox::critical(0, "Error", "Not connected to server.",
									  QMessageBox::Ok);
				ServerDisconnect();	// stop timer
				return false;
			}
			return true;
		}

		void ShowMessage(const char* pcMsg, bool bTemp=false)
		{
			if(!statusbar) return;

			if(bTemp)
				statusbar->showMessage(pcMsg);
			else
				pStatusMsg->setText(pcMsg);
		}

		void ShowTitleMessage(const char* pcMsg)
		{
			if(pcMsg==0)
				return;

			std::string strMsg = pcMsg;
			strMsg = trim(strMsg);
			if(strMsg=="")
			{
				setWindowTitle(QString(m_strTitle.c_str()).simplified());
				return;
			}

			std::string strNewTitle = m_strTitle;
			strNewTitle += std::string(" - ");
			strNewTitle += strMsg;

			setWindowTitle(QString(strNewTitle.c_str()));
		}

		// iCnts or iClients set to -1 means: do not update respective value
		void ShowRightMessage(int iCnts=-1, int iClients=-1, int iRunning=-1,
							  int iTotalCounts=-1)
		{
			static int iLastCnts=0,
					   iLastClients=0,
					   iLastRunning=0,
					   iLastTotalCounts=0;

			if(iCnts!=-1)
				iLastCnts = iCnts;
			if(iClients!=-1)
				iLastClients = iClients;
			if(iRunning!=-1)
				iLastRunning = iRunning;
			if(iTotalCounts!=-1)
				iLastTotalCounts = iTotalCounts;

			std::ostringstream ostr;
			SetNumberGrouping(ostr);

			std::string strTotalCounts =
					(m_cascadewidget.IsRoiInUse() ? "Counts (ROI): "
												  : "Counts (Total): ");

			ostr << strTotalCounts << iLastTotalCounts
				 /*<< ", Ext. Counts: " << iLastCnts*/
				 << ", Clients: " << iLastClients
				 << ", Measurement " << (iLastRunning?"running":"not running");

			if(ostr.str() != pStatusExtCount->text().toAscii().data())
			{ // set new status
				pStatusExtCount->setText(ostr.str().c_str());
			}
		}

		void UpdateLabels(bool bUpdateWidgetLabels=true)
		{
			if(bUpdateWidgetLabels)
				m_cascadewidget.UpdateLabels();

			if(m_cascadewidget.IsTofLoaded())
			{
				sliderFolien->setEnabled(true);
				labelFolie->setEnabled(true);

				switch(m_cascadewidget.GetMode())
				{
					case MODE_SLIDES:
					case MODE_SUMS:
					case MODE_OVERVIEW:
						sliderZeitkanaele->setEnabled(true);
						labelZeitkanal->setEnabled(true);
						break;

					case MODE_PHASES:
					case MODE_PHASESUMS:
						sliderZeitkanaele->setEnabled(false);
						labelZeitkanal->setEnabled(false);
						break;

					case MODE_CONTRASTS:
					case MODE_CONTRASTSUMS:
						sliderZeitkanaele->setEnabled(false);
						labelZeitkanal->setEnabled(false);
						break;
				}

				// Statuszeile aktualisieren
				switch(m_cascadewidget.GetMode())
				{
					case MODE_SLIDES:
						ShowMessage("Showing Foils.");
						break;
					case MODE_SUMS:
						ShowMessage("Showing Sums.");
						break;

					case MODE_OVERVIEW:
						ShowMessage("Showing Overview.");
						break;

					case MODE_PHASES:
						ShowMessage("Showing Phases.");
						break;
					case MODE_PHASESUMS:
						ShowMessage("Showing Phase Sums.");
						break;

					case MODE_CONTRASTS:
						ShowMessage("Showing Contrasts.");
						break;
					case MODE_CONTRASTSUMS:
						ShowMessage("Showing Contrast Sums.");
						break;
				}
			}
			else if(m_cascadewidget.IsPadLoaded())
			{
				sliderFolien->setEnabled(false);
				labelFolie->setEnabled(false);
				sliderZeitkanaele->setEnabled(false);
				labelZeitkanal->setEnabled(false);
				ShowMessage("Showing PAD.");
			}
		}

		void UpdateSliders()
		{
			const TofConfig& conf = GlobalConfig::GetTofConfig();

			sliderFolien->setMaximum(conf.GetFoilCount()-1);
			sliderZeitkanaele->setMaximum(conf.GetImagesPerFoil()-1);
		}

	// Slots
	protected slots:
		void FileHasChanged(const char* pcFile=0)
		{
			int iCounts = m_cascadewidget.GetCounts();
			ShowRightMessage(-1,-1,-1,iCounts);

			if(pcFile)
			{
				ShowTitleMessage(pcFile);
				//actionViewsOverview->setChecked(true);
			}
		}

		/////////// Slot für Tcp-Client ////////////////////////////////////////
		void ServerMessageSlot(const char* pcBuf, int iLen)
		{
			// Antworten müssen mindestens 4 Zeichen lang sein (Kommandostring)
			if(iLen<4) return;

			const TofConfig& conf = GlobalConfig::GetTofConfig();

			////////////////////////////////////////////////////////////////////
			// PAD-Daten vorhanden
			if(!strncmp(pcBuf,"IMAG",4))
			{
				// if global config changed
				bool bForceReinit = false;

	#ifndef DATA_COMPRESSED
				// Abfrage nur für unkomprimierte Daten möglich
				if(iLen-4 != (int)sizeof(int)*conf.GetImageHeight()
											 *conf.GetImageWidth())
				{
					bForceReinit = true;

					// Dimensionen stimmen nicht, neue raten
					if(!GlobalConfig::GuessConfigFromSize(0,(iLen-4)/4,
																		false))
					{
						static bool bMsgShown = false;
						
						QString strMsg("Dimension mismatch in PAD data!\n"
								"Client expected: %1 bytes\n"
								"Server sent: %2 bytes");

						strMsg = strMsg.arg((int)sizeof(int)*
								conf.GetImageHeight()*
								conf.GetImageWidth()).arg(iLen-4);

						if(!bMsgShown)
						{
							QMessageBox::critical(0, "Cascade - Server", strMsg,
															QMessageBox::Ok);

							bMsgShown = true;
						}

						strMsg.replace("\n", ", ");
						logger.SetCurLogLevel(LOGLEVEL_ERR);
						logger << "Main: " << strMsg.toAscii().data() << ".\n";
						return;
					}
				}
	#endif
				if(bForceReinit)
					m_cascadewidget.ForceReinit();
				void* pvData = m_cascadewidget.NewPad();
	#ifdef DATA_COMPRESSED
				// Komprimierte Daten umkopieren
				int iLenOut = sizeof(int)*conf.IMAGE_HEIGHT*
										  conf.IMAGE_WIDTH;
				if(!zlib_decompress(pcBuf+4, iLen-4, pvData, iLenOut))
				{
					QMessageBox::critical(0, "Cascade - Server",
										  "Error in PAD decompression.",
										  QMessageBox::Ok);
					return;
				}
	#else
				// Unkomprimierte Daten umkopieren
				memcpy(pvData, pcBuf+4, sizeof(int)*
										conf.GetImageHeight()*
										conf.GetImageWidth());
	#endif

				m_cascadewidget.UpdateRange();
				m_cascadewidget.UpdateGraph();

				UpdateLabels(false);
				FileHasChanged();

				//ShowMessage("PAD loaded from Server.");
			}
			////////////////////////////////////////////////////////////////////
			// TOF-Daten vorhanden
			else if(!strncmp(pcBuf,"DATA",4))
			{
				// if global config changed
				bool bForceReinit = false;

	#ifndef DATA_COMPRESSED
				int iExpectedSize = conf.GetPseudoCompression()
								? sizeof(int) * conf.GetFoilCount()*
								  conf.GetImagesPerFoil()*
								  conf.GetImageHeight()*
								  conf.GetImageWidth()
								: sizeof(int) * conf.GetImageCount()*
								  conf.GetImageHeight()*
								  conf.GetImageWidth();

				if(iLen-4 != iExpectedSize)
				{
					bForceReinit = true;

					// Dimensionen stimmen nicht, neue raten
					if(!GlobalConfig::GuessConfigFromSize(
						m_cascadewidget.GetTof()->
						GetTofConfig().GetPseudoCompression(),
								(iLen-4)/4, true))
					{
						static bool bMsgShown = false;
						
						QString strMsg("Dimension mismatch in TOF data!\n"
									   "Client expected: %1 bytes\n"
									   "Server sent: %2 bytes");

						strMsg = strMsg.arg(iExpectedSize).arg(iLen-4);

						if(!bMsgShown)
						{
							QMessageBox::critical(0, "Cascade - Server", strMsg,
												QMessageBox::Ok);

							bMsgShown = true;
						}

						strMsg.replace("\n", ", ");
						logger << "Main: " << strMsg.toAscii().data() << ".\n";
						return;
					}
				}
	#endif
				if(bForceReinit)
					m_cascadewidget.ForceReinit();
				void* pvData = m_cascadewidget.NewTof();

	#ifdef DATA_COMPRESSED
				// Komprimierte Daten umkopieren
				int iLenOut = sizeof(int)*conf.IMAGE_COUNT*
										  conf.IMAGE_HEIGHT*
										  conf.IMAGE_WIDTH;
				if(!zlib_decompress(pcBuf+4, iLen-4, pvData, iLenOut))
				{
					QMessageBox::critical(0, "Cascade - Server",
								"Error in TOF decompression.", QMessageBox::Ok);
					return;
				}
	#else
				// Unkomprimierte Daten umkopieren
				memcpy(pvData, pcBuf+4, iExpectedSize);
	#endif

				//m_cascadewidget.ShowGraph();	// macht viewOverview schon
				//UpdateLabels(false);

				UpdateSliders();
				FileHasChanged();

				//ShowMessage("TOF loaded from Server.");

				//viewOverview();
				//actionViewsOverview->setChecked(true);

				m_cascadewidget.UpdateGraph();
			}
			////////////////////////////////////////////////////////////////////
			// Fehler
			else if(!strncmp(pcBuf,"ERR_",4))
			{
				QMessageBox::critical(0, "Cascade - Server", pcBuf+4,
									  QMessageBox::Ok);
			}
			// Status-Update erhalten
			else if(!strncmp(pcBuf,"MSG_",4))
			{
				ArgumentMap args(pcBuf+4);

				// stop?
				std::pair<bool, int> pairStop = args.QueryInt("stop",1);
				if(pairStop.first)
					ShowRightMessage(-1,-1,!pairStop.second);

				// xres?
				std::pair<bool, int> pairXRes =
							args.QueryInt("xres", ServerCfgDlg::GetStatXRes());
				if(pairXRes.first)
				{
					ServerCfgDlg::SetStatXRes(pairXRes.second);

					TofConfig& conf = GlobalConfig::GetTofConfig();
					conf.SetImageWidth(pairXRes.second);
				}

				// yres?
				std::pair<bool, int> pairYRes =
							args.QueryInt("yres", ServerCfgDlg::GetStatYRes());
				if(pairYRes.first)
				{
					ServerCfgDlg::SetStatYRes(pairYRes.second);

					TofConfig& conf = GlobalConfig::GetTofConfig();
					conf.SetImageHeight(pairYRes.second);
				}

				// tres?
				std::pair<bool, int> pairTRes =
							args.QueryInt("tres", ServerCfgDlg::GetStatTRes());
				if(pairTRes.first)
				{
					ServerCfgDlg::SetStatTRes(pairTRes.second);

					TofConfig& conf = GlobalConfig::GetTofConfig();
					conf.SetImageCount(pairTRes.second);
				}

				// measurement time?
				std::pair<bool, double> pairTime = args.QueryDouble("time",
										ServerCfgDlg::GetStatTime());
				if(pairTime.first)
					ServerCfgDlg::SetStatTime(pairTime.second);

				// mode?
				const char* pcMode = args.QueryString("mode");
				if(pcMode)
				{
					if(strcasecmp(pcMode, "tof")==0)
						ServerCfgDlg::SetStatMode(MODE_TOF);
					else if(strcasecmp(pcMode, "image")==0)
						ServerCfgDlg::SetStatMode(MODE_PAD);
				}

				// pseudo-compression?
				std::pair<bool, int> pairComp = args.QueryInt("comp",1);
				if(pairComp.first)
				{
					TofConfig& conf = GlobalConfig::GetTofConfig();

					conf.SetPseudoCompression(pairComp.second);
					ServerCfgDlg::SetStatComp(pairComp.second);
				}

				std::pair<bool, int> pairCnt = args.QueryInt("ext_count",0);
				if(pairCnt.first)
					ShowRightMessage(pairCnt.second);

				std::pair<bool, int> pairClients = args.QueryInt("clients",0);
				if(pairClients.first)
					ShowRightMessage(-1, pairClients.second);


				// if global config changed, reinit PAD & TOF memory
				if(pairXRes.first || pairYRes.first || pairTRes.first ||
									 pairComp.first)
					m_cascadewidget.ForceReinit();
			}
			else if(!strncmp(pcBuf,"OKAY",4))
			{}
			else
			{
				logger.SetCurLogLevel(LOGLEVEL_ERR);
				logger << "Main: Unknown prefix in server response: \""
					   << pcBuf[0]<<pcBuf[1]<<pcBuf[2]<<pcBuf[3]
					   << "\".\n";
			}
		}

		// Slot vom Summen-Dialog
		void FolienSummeSlot(const bool *pbKanaele, int iMode)
		{
			switch(iMode)
			{
				case MODE_SLIDES:
				case MODE_SUMS:
				case MODE_OVERVIEW:
					actionViewsSlides->setChecked(true);
					break;

				case MODE_PHASES:
				case MODE_PHASESUMS:
					actionViewsPhases->setChecked(true);
					break;

				case MODE_CONTRASTS:
				case MODE_CONTRASTSUMS:
					actionViewsContrasts->setChecked(true);
					break;
			}
			UpdateLabels(false);
		}

		// Callback vom Folien-Slider
		void ChangeFolie(int iVal)
		{
			if(!m_cascadewidget.IsTofLoaded()) return;

			switch(m_cascadewidget.GetMode())
			{
				case MODE_OVERVIEW:
				case MODE_SUMS:
					actionViewsSlides->setChecked(true);
					m_cascadewidget.SetMode(MODE_SLIDES);
					break;
				case MODE_PHASESUMS:
					actionViewsPhases->setChecked(true);
					m_cascadewidget.SetMode(MODE_PHASES);
					break;
				case MODE_CONTRASTSUMS:
					actionViewsContrasts->setChecked(true);
					m_cascadewidget.SetMode(MODE_CONTRASTS);
					break;
			}

			m_cascadewidget.SetFoil(iVal);
			m_cascadewidget.UpdateGraph();
			UpdateLabels(false);

			QString strFoil("Foil (%1):");
			strFoil = strFoil.arg(m_cascadewidget.GetFoil()+1);
			labelFolie->setText(strFoil);
		}

		// Callback vom Kanal-Slider
		void ChangeZeitkanal(int iVal)
		{
			if(!m_cascadewidget.IsTofLoaded()) return;

			switch(m_cascadewidget.GetMode())
			{
				case MODE_OVERVIEW:
				case MODE_SUMS:
					actionViewsSlides->setChecked(true);
					m_cascadewidget.SetMode(MODE_SLIDES);
					break;
				case MODE_PHASESUMS:
					actionViewsPhases->setChecked(true);
					m_cascadewidget.SetMode(MODE_PHASES);
					break;
				case MODE_CONTRASTSUMS:
					actionViewsContrasts->setChecked(true);
					m_cascadewidget.SetMode(MODE_CONTRASTS);
					break;
			}

			m_cascadewidget.SetTimechannel(iVal);
			m_cascadewidget.UpdateGraph();
			UpdateLabels(false);

			QString strTC("Time Channel (%1):");
			strTC = strTC.arg(m_cascadewidget.GetTimechannel()+1);
			labelZeitkanal->setText(strTC);
		}

		void SetLog10(bool bLog)
		{
			m_cascadewidget.SetLog10(bLog);
			UpdateLabels(false);
		}

		void SetAutoFetch(bool bAutoFetch)
		{
			if(bAutoFetch)
				m_autofetchtimer.start(AUTOFETCH_POLL_TIME);
			else
				m_autofetchtimer.stop();
		}

		void AutoFetch()
		{
			if(!m_client.isconnected())
			{
				//SetAutoFetch(false);
				//btnAutoFetch->setChecked(false);
				return;
			}
			m_client.sendmsg("CMD_readsram");
		}

		void showCalibration(void)
		{
			if(!m_cascadewidget.IsTofLoaded())
			{
				QMessageBox::critical(0, "Calibration", "No TOF loaded "
										"or not in TOF mode.", QMessageBox::Ok);
				return;
			}

			m_cascadewidget.showCalibrationDlg(NUM_BINS);
		}

		void showGraph(void)
		{
			if(!m_cascadewidget.IsTofLoaded())
			{
				QMessageBox::critical(0, "Graph", "No TOF loaded "
										"or not in TOF mode.", QMessageBox::Ok);
				return;
			}

			m_cascadewidget.showGraphDlg();
		}

		void showSummenDialog(void)
		{
			if(!m_cascadewidget.IsTofLoaded())
			{
				QMessageBox::critical(0, "Sums", "No TOF loaded "
										"or not in TOF mode.", QMessageBox::Ok);
				return;
			}

			m_cascadewidget.showSumDlg();
		}

		void showIntegrationDialog()
		{
			if(!m_cascadewidget.IsTofLoaded() && !m_cascadewidget.IsPadLoaded())
			{
				QMessageBox::critical(0, "Integration", "No TOF or PAD loaded.",
									  QMessageBox::Ok);
				return;
			}

			m_cascadewidget.showIntegrationDlg();
		}

		void viewOverview()
		{
			m_cascadewidget.viewOverview();
			UpdateLabels(false);
		}

		void viewSlides()
		{
			m_cascadewidget.viewSlides();
			UpdateLabels(false);
		}

		void viewPhases()
		{
			m_cascadewidget.viewPhases();
			UpdateLabels(false);
		}

		void viewContrasts()
		{
			m_cascadewidget.viewContrasts();
			UpdateLabels(false);
		}

		////////////////////////// Server Menu Items ///////////////////////////
		void ConnectToServer()
		{
			ServerDlg SrvDlg(this);

			// get default settings from config file
			QString strConfigAddress =
						QString(Config::GetSingleton()->QueryString(
						"/cascade_config/server/address",
						"127.0.0.1").c_str()).simplified();

			int iConfigPort = Config::GetSingleton()
						->QueryInt("/cascade_config/server/port", 1234);


			static QString strLastAddress("");
			static int iLastPort = 0;

			// no previous address entered
			if(strLastAddress==QString("") || iLastPort==0)
			{
				SrvDlg.editAddress->setText(strConfigAddress);

				QString strPort;
				strPort.setNum(iConfigPort);
				SrvDlg.editPort->setText(strPort);
			}
			else 								// use previous address
			{
				SrvDlg.editAddress->setText(strLastAddress);

				QString strPort;
				strPort.setNum(iLastPort);
				SrvDlg.editPort->setText(strPort);
			}

			if(SrvDlg.exec() == QDialog::Accepted)
			{
				ServerDisconnect();

				if(!m_client.connecttohost(
						SrvDlg.editAddress->text().toAscii().data(),
						SrvDlg.editPort->text().toInt()))
				{
					QString strBuf("Could not connect to server\n"
								   "\"%1\"\nat port %2.");
					strBuf = strBuf.arg(SrvDlg.editAddress->text()).
									arg(SrvDlg.editPort->text()).
									arg(SrvDlg.editPort->text());
					
					QMessageBox::critical(0, "Error", strBuf, QMessageBox::Ok);
					return;
				}

				// show messages
				ShowMessage("Connected to server.");

				std::string strTitleMsg
								= SrvDlg.editAddress->text().toAscii().data();
				strTitleMsg += ":";
				strTitleMsg += SrvDlg.editPort->text().toAscii().data();
				ShowTitleMessage(strTitleMsg.c_str());
				// -------------

				m_statustimer.start(SERVER_STATUS_POLL_TIME);

				strLastAddress = SrvDlg.editAddress->text();
				iLastPort = SrvDlg.editPort->text().toInt();

				// get current config of hardware
				GetServerConfig();
			}
		}

		void ServerDisconnect()
		{
			m_statustimer.stop();
			m_client.disconnect();
			ShowMessage("Disconnected from server.");
			ShowTitleMessage("");
			ShowRightMessage(0,0,0);
		}

		// enter manual server command
		void ServerCommand()
		{
			if(!CheckConnected()) return;

			CommandDlg commanddlg(this);
			if(commanddlg.exec() == QDialog::Accepted)
			{
				QString strCmd = commanddlg.editCommand->text().simplified();
				if(strCmd != QString(""))
					m_client.sendmsg(strCmd.toAscii().data());
			}
		}

		void ServerStatus()
		{
			if(!CheckConnected()) return;

			m_client.sendmsg("CMD_status_cdr");
			m_client.sendmsg("CMD_status_server");
		}

		void ServerMeasurementStart()
		{
			if(!CheckConnected()) return;

			m_client.sendmsg("CMD_start");
		}

		void ServerMeasurementStop()
		{
			if(!CheckConnected()) return;

			m_client.sendmsg("CMD_stop");
		}

		void LoadTofServer()
		{
			if(!CheckConnected()) return;

			m_client.sendmsg("CMD_readsram");
		}

		void GetServerConfig()
		{
			if(!CheckConnected()) return;

			m_client.sendmsg("CMD_getconfig_cdr");
		}

		void ServerConfig()
		{
			if(!CheckConnected()) return;

			ServerCfgDlg srvcfgdlg(this);

			if(srvcfgdlg.exec()==QDialog::Accepted)
			{
				double dTime = srvcfgdlg.GetMeasTime();
				unsigned int iXRes = srvcfgdlg.GetXRes();
				unsigned int iYRes = srvcfgdlg.GetYRes();
				unsigned int iTRes = srvcfgdlg.GetTRes();
				bool bComp = srvcfgdlg.GetPseudoComp();

				TofConfig& conf = GlobalConfig::GetTofConfig();
				conf.SetImageWidth(iXRes);
				conf.SetImageHeight(iYRes);
				conf.SetImageCount(iTRes);
				conf.SetPseudoCompression(bComp);

				// reinit PAD & TOF memory
				m_cascadewidget.ForceReinit();

				const char* pcMode = "";
				switch(srvcfgdlg.GetMode())
				{
					case MODE_PAD:
						pcMode = "image";
						break;
					case MODE_TOF:
						pcMode = "tof";
						break;
				}
				char pcMsg[256];
				sprintf(pcMsg, "CMD_config_cdr "
							   "time=%f xres=%d yres=%d tres=%d "
							   "mode=%s comp=%d",
							   dTime, iXRes, iYRes, iTRes, pcMode, bComp);
				m_client.sendmsg(pcMsg);
			}
		}
		////////////////////////////////////////////////////////////////////////


		///////////////////////////// File Menu Items /////////////////////////
		void GarbageCollect()
		{
			gc.gc();
			gc.print();
		}

		void ShowMemUsage()
		{
			GcDlg gcdlg(this);
			gcdlg.exec();
		}

		void BrowseFiles()
		{
			ServerDisconnect();
			m_cascadewidget.showBrowseDlg();
		}

		void LoadPad(bool bBinary)
		{
			QString strCurDir(GlobalConfig::GetCurDir().c_str());

			QString strFile = QFileDialog::getOpenFileName(this,
											"Open PAD File",
											QString(strCurDir),
											"PAD Files (*.pad *.PAD);;All Files (*)");

			if(strFile=="")
				return;

			// set current directory
			QDir dir(strFile);
			dir.cdUp();
			GlobalConfig::SetCurDir(dir.absolutePath().toAscii().data());

			bool bOk;
			if(bBinary)
				bOk = m_cascadewidget.LoadPadFile(strFile.toAscii().data());
			else
				bOk = m_cascadewidget.LoadPadFileTxt(strFile.toAscii().data());

			if(bOk)
			{
				ServerDisconnect();
				//m_cascadewidget.UpdateGraph();

				FileHasChanged(strFile.toAscii().data());

				UpdateLabels(false);
				ShowMessage("PAD loaded.");
			}
		}

		void LoadPad() { LoadPad(1); }
		void LoadPadTxt() { LoadPad(0); }

		void LoadTof()
		{
			QString strCurDir(GlobalConfig::GetCurDir().c_str());

			QString strFile = QFileDialog::getOpenFileName(
								this, "Open TOF File", strCurDir,
								"TOF Files (*.tof *.TOF);;All Files (*)");

			if(strFile=="")
				return;

			// set current directory
			QDir dir(strFile);
			dir.cdUp();
			GlobalConfig::SetCurDir(dir.absolutePath().toAscii().data());

			if(m_cascadewidget.LoadTofFile(strFile.toAscii().data()))
			{
				ServerDisconnect();

				//m_cascadewidget.UpdateGraph();	// macht viewOverview schon

				FileHasChanged(strFile.toAscii().data());

				UpdateLabels(false);
				UpdateSliders();
				ShowMessage("TOF loaded.");

				//viewOverview();
				//actionViewsOverview->setChecked(true);
			}
		}

		void SaveFile()
		{
			// PAD
			if(m_cascadewidget.IsPadLoaded())
			{
				QString strFile = QFileDialog::getSaveFileName(this,
									"Save as PAD File", "",
									"PAD Files (*.pad *.PAD);;All Files (*)");
				if(strFile=="")
					return;

				m_cascadewidget.GetPad()->SaveFile(strFile.toAscii().data());
			}
			if(m_cascadewidget.IsTofLoaded())
			{
				QString strFile = QFileDialog::getSaveFileName(this,
									"Save as TOF File", "",
									"TOF Files (*.tof *.TOF);;All Files (*)");
				if(strFile=="")
					return;

				m_cascadewidget.GetTof()->SaveFile(strFile.toAscii().data());
			}
		}

		void SaveFileAsDat()
		{
			if(!m_cascadewidget.IsPadLoaded() && !m_cascadewidget.IsTofLoaded())
				return;
			
			QString strFile = QFileDialog::getSaveFileName(this,
								"Save as DAT File", "",
								"DAT Files (*.dat *.DAT);;All Files (*)");
			// PAD
			if(m_cascadewidget.IsPadLoaded())
			{
				m_cascadewidget.GetPad()->SaveAsDat(strFile.toAscii().data());
			}
			if(m_cascadewidget.IsTofLoaded())
			{
				m_cascadewidget.GetTof()->SaveAsDat(strFile.toAscii().data());
			}
		}		

		void WriteXML(void)
		{
			if(!m_cascadewidget.IsTofLoaded() && !m_cascadewidget.IsPadLoaded())
				return;

			QString strFile = QFileDialog::getSaveFileName(this,
								"Save as XML File", "",
								"XML Files (*.xml *.XML);;All Files (*)");
			if(strFile=="")
				return;

			TmpImage tmpimg;
			if(m_cascadewidget.IsTofLoaded())	// TOF-Datei offen
				tmpimg = m_cascadewidget.GetTof()->GetOverview();
			else					// PAD-Datei offen
				tmpimg.ConvertPAD(m_cascadewidget.GetPad());
			tmpimg.WriteXML(strFile.toAscii().data());
		}
		///////////////////////////////////////////////////////////////////

		//////////////////////////ROI /////////////////////////////////////
		void showRoiDlg()
		{
			if(!m_cascadewidget.IsTofLoaded() && !m_cascadewidget.IsPadLoaded())
			{
				QMessageBox::critical(0, "ROI", "No TOF or PAD loaded.",
									  QMessageBox::Ok);
				return;
			}

			m_cascadewidget.showRoiDlg();
		}

		void ClearRoi()
		{
			m_cascadewidget.ClearRoi();
		}

		void LoadRoi()
		{
			if(!m_cascadewidget.IsTofLoaded() && !m_cascadewidget.IsPadLoaded())
			{
				QMessageBox::critical(0, "ROI", "No TOF or PAD loaded.",
									  QMessageBox::Ok);
				return;
			}

			QString strFile = QFileDialog::getOpenFileName(this,
							"Open ROI File","",
							"ROI Files (*.roi *.ROI);;XML Files (*.xml *.XML);;"
							"All Files (*)");
			if(strFile!="" && m_cascadewidget.LoadRoi(strFile.toAscii().data()))
			{
				UpdateLabels(false);
				ShowMessage("ROI loaded.");
			}
		}

		void SaveRoi()
		{
			if(!m_cascadewidget.IsTofLoaded() && !m_cascadewidget.IsPadLoaded())
			{
				QMessageBox::critical(0, "ROI", "No TOF or PAD loaded.",
									  QMessageBox::Ok);
				return;
			}

			QString strFile = QFileDialog::getSaveFileName(this,
							"Save ROI File", "",
							"ROI Files (*.roi *.roi);;XML Files (*.xml *.XML);;"
							"All Files (*)");
			if(strFile=="")
				return;

			if(m_cascadewidget.SaveRoi(strFile.toAscii().data()))
			{
				UpdateLabels(false);
				ShowMessage("ROI saved.");
			}
		}

		////////////////////////// ROI Toolbar ////////////////////////////
		void toolZoom()
		{ m_cascadewidget.SetRoiDrawMode(ROI_DRAW_NONE); }
		void toolRect()
		{ m_cascadewidget.SetRoiDrawMode(ROI_DRAW_RECT); }
		void toolCircle()
		{ m_cascadewidget.SetRoiDrawMode(ROI_DRAW_CIRC); }
		void toolEllipse()
		{ m_cascadewidget.SetRoiDrawMode(ROI_DRAW_ELLIPSE); }
		void toolCircRing()
		{ m_cascadewidget.SetRoiDrawMode(ROI_DRAW_CIRCRING); }
		void toolCircSeg()
		{ m_cascadewidget.SetRoiDrawMode(ROI_DRAW_CIRCSEG); }
		void toolPolygon()
		{ m_cascadewidget.SetRoiDrawMode(ROI_DRAW_POLYGON); }
		///////////////////////////////////////////////////////////////////


		///////////////////////// Tool Menu Items /////////////////////////

		void GenerateRandomTof()
		{
			m_cascadewidget.NewTof();
			TofImage *pTof = m_cascadewidget.GetTof();
			pTof->GenerateRandomData();

			//m_cascadewidget.UpdateGraph();
			FileHasChanged();

			UpdateLabels(false);
			UpdateSliders();
			ShowMessage("TOF generated.");

			viewOverview();
			actionViewsOverview->setChecked(true);
		}

		void GenerateRandomPad()
		{
			m_cascadewidget.NewPad();
			PadImage *pPad = m_cascadewidget.GetPad();
			pPad->GenerateRandomData();


			m_cascadewidget.UpdateRange();
			m_cascadewidget.UpdateGraph();
			FileHasChanged();

			UpdateLabels(false);
			ShowMessage("PAD generated.");
		}

		void BatchJob()
		{
			BatchDlg dlg(&m_cascadewidget);
			dlg.exec();
		}

		void AreaPhaseCorrect()
		{
			if(!m_cascadewidget.IsTofLoaded())
				return;

			TofImage* pTof = m_cascadewidget.GetTof();
			if(pTof->AreaPhaseCorrect())
				m_cascadewidget.UpdateGraph();
		}

		void PrintLocalConf()
		{
			const CascConf* pConf = 0;
			std::string strFileType;
			
			if(m_cascadewidget.IsTofLoaded())
			{
				strFileType = "TOF";
				
				const TofImage* pTof = m_cascadewidget.GetTof();
				pConf = &pTof->GetLocalConfig();
			}
			else if(m_cascadewidget.IsPadLoaded())
			{
				strFileType = "PAD";
				
				const PadImage* pPad = m_cascadewidget.GetPad();
				pConf = &pPad->GetLocalConfig();
			}

			if(pConf)
			{
				std::ostringstream ostr;
				ostr << (*pConf);

				std::string str = ostr.str();
				
				logger.SetCurLogLevel(LOGLEVEL_INFO);
				if(str != "")
				{
					logger << "--------------------------------------------------------------------------------\n";
					logger << "Local configuration for " << strFileType << " file\n";
					logger << ostr.str();
					logger << "--------------------------------------------------------------------------------\n";
				}
				else
					logger << "<no local configuration available>\n";
			}
			else
			{
				logger << "<no file loaded>\n";
			}
		}
		//////////////////////////////////////////////////////////////////


		///////////////////////// Help ///////////////////////////////////
		void About()
		{
			QString strAbout = "Cascade Viewer written by Tobias Weber, 2010-2012.";
			strAbout += "\n";

			#if defined(CASCADE_VIEVER_VERSION)
			strAbout += "\nVersion: " + QString(CASCADE_VIEVER_VERSION);
			#endif

			#if defined(__DATE__) && defined(__TIME__)
			strAbout += QString("\n") + QString("Build time: ") +
						QString(__DATE__) + QString(" ") + QString(__TIME__);
			#endif

			#ifdef __VERSION__
			strAbout += QString("\n") + QString("Built with CC version ") +
						QString(__VERSION__);
			#endif
			strAbout += "\n";

			#ifdef QT_VERSION_STR
			strAbout += QString("\n") + QString("Uses Qt version ") +
						QString(QT_VERSION_STR) + QString("\thttp://qt.nokia.com");
			#endif

			#ifdef QWT_VERSION_STR
			strAbout += QString("\n") + QString("Uses Qwt version ") +
						QString(QWT_VERSION_STR) + QString("\thttp://qwt.sf.net");
			#endif

			#ifdef USE_MINUIT
			strAbout += QString("\n") + QString("Uses Minuit 2\t\thttp://root.cern.ch");
			#endif

			#ifdef USE_FFTW
			strAbout += QString("\n") + QString("Uses FFTW 3\t\thttp://www.fftw.org");
			#endif

			#ifdef USE_XML
			strAbout += QString("\n") + QString("Uses libxml 2\t\thttp://xmlsoft.org");
			#endif

			strAbout += "\n\n";
			strAbout += "This program is free software; you can redistribute it and/or modify it under\n"
						"the terms of the GNU General Public License as published by the Free Software\n"
						"Foundation; either version 2 of the License, or (at your option) any later\n"
						"version.\n\n"

						"This program is distributed in the hope that it will be useful, but WITHOUT\n"
						"ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n"
						"or FITNESS FOR A PARTICULAR PURPOSE.\n"
						"See the GNU General Public License for more details.\n\n"

						"You should have received a copy of the GNU General Public License along with\n"
						"this program; if not, write to the Free Software Foundation, Inc.,\n"
						"59 Temple Place, Suite 330, Boston, MA  02111-1307  USA\n";

			QMessageBox::about(this, "About", strAbout);
		}
		void AboutQt() { QMessageBox::aboutQt(this); }
		///////////////////////////////////////////////////////////////////

	public:
		virtual ~MainWindow()
		{
			Unload();
		}

		MainWindow(QWidget *parent=NULL)
			: QMainWindow(parent), m_cascadewidget(this),
			  m_client(this, false), m_statustimer(this), m_autofetchtimer(this),
			  statusbar(NULL)
		{
			m_strTitle = "Cascade Viewer";
			setWindowTitle(m_strTitle.c_str());

			m_cascadewidget.SetLog10(true);

			QWidget *pCentralWidget = new QWidget(this);
			setCentralWidget(pCentralWidget);


			//------------------------------------------------------------------
			//QGroupBox *grouptopright = new QGroupBox(&m_cascadewidget);
			//QGroupBox *groupbottomright = new QGroupBox(&m_cascadewidget);
			QGroupBox *groupbottomleft = new QGroupBox(pCentralWidget);

			QGridLayout *pLayoutBL = new QGridLayout(groupbottomleft);

			labelFolie = new QLabel(groupbottomleft);
			pLayoutBL->addWidget(labelFolie, 0, 0, 1, 1);

			sliderFolien = new QSlider(groupbottomleft);
			sliderFolien->setOrientation(Qt::Horizontal);
			sliderFolien->setMinimum(0);
			sliderFolien->setValue(0);
			labelFolie->setText("Foil:");
			labelFolie->setMinimumWidth(100);
			//ChangeFolie(0);
			pLayoutBL->addWidget(sliderFolien, 0, 1, 1, 1);

			labelZeitkanal = new QLabel(groupbottomleft);
			pLayoutBL->addWidget(labelZeitkanal, 1, 0, 1, 1);

			sliderZeitkanaele = new QSlider(groupbottomleft);
			sliderZeitkanaele->setOrientation(Qt::Horizontal);
			sliderZeitkanaele->setMinimum(0);

			sliderZeitkanaele->setValue(0);
			labelZeitkanal->setText("Time Channel:");
			labelZeitkanal->setMinimumWidth(100);
			//ChangeZeitkanal(0);
			UpdateSliders();

			pLayoutBL->addWidget(sliderZeitkanaele, 1, 1, 1, 1);
			//------------------------------------------------------------------



			//------------------------------------------------------------------
			QGridLayout *centralgridlayout = new QGridLayout(pCentralWidget);
			centralgridlayout->addWidget(&m_cascadewidget, 0, 0, 1, 1);
			//centralgridlayout->addWidget(grouptopright, 0, 1, 1, 1);
			//centralgridlayout->addWidget(groupbottomright, 1, 1, 1, 1);
			centralgridlayout->addWidget(groupbottomleft, 1, 0, 1, 1);
			//------------------------------------------------------------------



			//------------------------------------------------------------------
			// Menu Items
			// File Menu Items
			QAction *actionBrowseFiles = new QAction(
						QIcon::fromTheme("system-file-manager"),
						"&Browse Files...",
						this);
			actionBrowseFiles->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_B));

			QAction *actionLoadPad = new QAction(
						QIcon::fromTheme("document-open"),
						"Load &PAD File...",
						this);
			QAction *actionLoadPadTxt = new QAction(
						QIcon::fromTheme("document-open"),
						"Load PAD File (Text)...",
						this);
			actionLoadPad->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_P));

			QAction *actionLoadTof = new QAction(
						QIcon::fromTheme("document-open"),
						"Load &TOF File...",
						this);
			actionLoadTof->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_T));

			QAction *actionShowFileParams = new QAction(
					QIcon::fromTheme("document-properties"),
					"Show &File Parameters...",
					this);

			QAction *actionSaveFile = new QAction(
						QIcon::fromTheme("document-save-as"),
						"&Save File...",
						this);
			QAction *actionSaveDatFile = new QAction(
						QIcon::fromTheme("document-save-as"),
						"&Save File as DAT...",
						this);			
			QAction *actionWriteXML = new QAction(
						QIcon::fromTheme("document-save-as"),
						"Write &XML...",
						this);
			QAction *actionPrint = new QAction(
						QIcon::fromTheme("document-print"),
						"P&rint Plot...",
						this);
			QAction *actionGc = new QAction(
						QIcon::fromTheme("user-trash-full"),
						"Garbage Collection",
						this);
			QAction *actionMem = new QAction(
						QIcon::fromTheme("utilities-system-monitor"),
						"Show Memory Usage...",
						this);
			QAction *actionExit = new QAction(
						QIcon::fromTheme("application-exit"),
						"&Exit",
						this);


			// Plot Menu Items
			QAction *actionCountRange = new QAction(
						"Change Count &Range...",
						this
						);


			// Server Menu Items
			QAction *actionConnectServer = new QAction(
						QIcon::fromTheme("network-wireless"),
						"&Connect to Server...",
						this);
			actionConnectServer->setShortcut(
						QKeySequence(Qt::CTRL + Qt::Key_C));

			QAction *actionServerDisconnect = new QAction(
						QIcon::fromTheme("network-offline"),
						"&Disconnect from Server",
						this);
			QAction *actionServerCommand = new QAction(
						QIcon::fromTheme("network-transmit"),
						"Enter &Manual Command...",
						this);

			QAction *actionServerMeasurementStart = new QAction(
						"&Start Measurement",
						this);
			actionServerMeasurementStart->setShortcut(
											QKeySequence(Qt::CTRL + Qt::Key_S));

			QAction *actionServerMeasurementStop = new QAction(this);
			actionServerMeasurementStop->setText("&End Measurement");

			QAction *actionLoadTofServer = new QAction(
						QIcon::fromTheme("network-receive"),
						"Fetch &Data",
						this);
			actionLoadTofServer->setShortcut(
						QKeySequence(Qt::CTRL + Qt::Key_D));

			QAction *actionConfigServer = new QAction(
						QIcon::fromTheme("preferences-system-network"),
						"C&onfigure...",
						this);

			QAction *actionConfigFromServer = new QAction(
						"&Retrieve Configuration",
						this);


			// Graph Menu Items
			QAction *actionGraph = new QAction(
						"&Counts vs. Time Channels...",
						this);
			QAction *actionSummen = new QAction(
						"&Sum Images...",
						this);
			QAction *actionCalibration = new QAction(
						"C&alibration...",
						this);

			QAction *actionIntegrate = new QAction(
						"&Integrate Radially...",
						this);
			QAction *actionCountsVsImages = new QAction(
						"&Counts vs. Images...",
						this);
			QAction *actionContrastsVsImages = new QAction(
						"C&ontrasts vs. Images...",
						this);


			// ROI Menu Items
			QAction *actionManageRois = new QAction(
						QIcon::fromTheme("list-add"),
						"&Manage ROI...",
						this);
			actionManageRois->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_R));

			QAction *actionLoadRoi = new QAction(
						QIcon::fromTheme("document-open"),
						"Load ROI...",
						this);
			QAction *actionSaveRoi = new QAction(
						QIcon::fromTheme("document-save-as"),
						"Save ROI...",
						this);
			QAction *actionClearRoi = new QAction(
						QIcon::fromTheme("edit-clear"),
						"Clear ROI",
						this);


			// Tool Menu Items
			QAction *actionGenerateRandomPad = new QAction("Generate Random &PAD", this);
			QAction *actionGenerateRandomTof = new QAction("Generate Random &TOF", this);
			QAction *actionBatchJob = new QAction("Run &Batch Job...", this);

			QAction *actionPrintLocalConf = new QAction("Print Local TOF/PAD Configuration", this);
			QAction *actionAreaPhaseCorrect = new QAction("Area-Phase Correction", this);

			// Help Menu Items
			QAction *actionAbout = new QAction(
						QIcon::fromTheme("help-about"),
						"&About...",
						this);
			QAction *actionAboutQt = new QAction(
						//QIcon::fromTheme("help-about"),
						"About &Qt...",
						this);
			//------------------------------------------------------------------


			//------------------------------------------------------------------
			// Menu Bar
			QMenuBar *menubar = new QMenuBar(this);;

			menubar->setGeometry(QRect(0, 0, 800, 25));
			QMenu *menuFile = new QMenu(menubar);
			menuFile->setTitle("&File");
			menuFile->addAction(actionLoadPad);
			menuFile->addAction(actionLoadPadTxt);
			menuFile->addAction(actionLoadTof);
			menuFile->addSeparator();
			menuFile->addAction(actionBrowseFiles);
			menuFile->addAction(actionShowFileParams);
			menuFile->addSeparator();
			menuFile->addAction(actionSaveFile);
			menuFile->addAction(actionSaveDatFile);
			menuFile->addAction(actionWriteXML);
			menuFile->addSeparator();
			menuFile->addAction(actionPrint);
			menuFile->addSeparator();
			menuFile->addAction(actionExit);
			menubar->addAction(menuFile->menuAction());

			QMenu *menuPlot = new QMenu(menubar);
			menuPlot->setTitle("&Plot");
			menuPlot->addAction(actionCountRange);
			menubar->addAction(menuPlot->menuAction());

			QMenu *menuServer = new QMenu(menubar);
			menuServer->setTitle("&Server");
			menuServer->addAction(actionConnectServer);
			menuServer->addAction(actionServerDisconnect);
			menuServer->addSeparator();
			menuServer->addAction(actionServerCommand);
			menuServer->addSeparator();
			menuServer->addAction(actionConfigFromServer);
			menuServer->addAction(actionConfigServer);
			menuServer->addSeparator();
			menuServer->addAction(actionServerMeasurementStart);
			menuServer->addAction(actionServerMeasurementStop);
			menuServer->addSeparator();
			menuServer->addAction(actionLoadTofServer);
			menubar->addAction(menuServer->menuAction());

			QMenu *menuGraph = new QMenu(menubar);
			menuGraph->setTitle("&Graphs");
			menuGraph->addAction(actionIntegrate);
			menuGraph->addAction(actionCountsVsImages);
			menubar->addAction(menuGraph->menuAction());

			QMenu *menuTofGraph = new QMenu(menubar);
			menuTofGraph->setTitle("&TOF Graphs");
			menuTofGraph->addAction(actionCalibration);
			menuTofGraph->addSeparator();
			menuTofGraph->addAction(actionGraph);
			menuTofGraph->addAction(actionContrastsVsImages);
			menuTofGraph->addAction(actionSummen);
			menubar->addAction(menuTofGraph->menuAction());

			QMenu *menuRoi = new QMenu(menubar);
			menuRoi->setTitle("&ROI");
			menuRoi->addAction(actionManageRois);
			menuRoi->addSeparator();
			menuRoi->addAction(actionLoadRoi);
			menuRoi->addAction(actionSaveRoi);
			menuRoi->addSeparator();
			menuRoi->addAction(actionClearRoi);
			menubar->addAction(menuRoi->menuAction());

			QMenu *menuTools = new QMenu(menubar);
			menuTools->setTitle("T&ools");
			menuTools->addAction(actionGenerateRandomPad);
			menuTools->addAction(actionGenerateRandomTof);
			menuTools->addSeparator();
			menuTools->addAction(actionBatchJob);
			menuTools->addSeparator();
			menuTools->addAction(actionPrintLocalConf);
			//menuTools->addAction(actionAreaPhaseCorrect);
			menuTools->addSeparator();
			menuTools->addAction(actionGc);
			menuTools->addAction(actionMem);
			menubar->addAction(menuTools->menuAction());

			QMenu *menuHelp = new QMenu(menubar);
			menuHelp->setTitle("&Help");
			menuHelp->addAction(actionAbout);
			menuHelp->addAction(actionAboutQt);
			menubar->addAction(menuHelp->menuAction());

			setMenuBar(menubar);
			//------------------------------------------------------------------


			//------------------------------------------------------------------
			// Directory Toolbar
			QToolBar *pDirToolbar = new QToolBar("File Toolbar", this);

			QAction *btnBrowse = new QAction(
										QIcon::fromTheme("system-file-manager"),
										QString("Browse Files..."),
										pDirToolbar);
			pDirToolbar->addAction(btnBrowse);

			addToolBar(pDirToolbar);
			//------------------------------------------------------------------


			//------------------------------------------------------------------
			// Plot Toolbar
			QToolBar *toolBar = new QToolBar("Plot Toolbar",this);

			btnLog = new QToolButton(toolBar);
			btnLog->setText("Log10");
			btnLog->setCheckable(true);
			btnLog->setChecked(m_cascadewidget.GetLog10());
			toolBar->addWidget(btnLog);

			btnAutoFetch = new QToolButton(toolBar);
			btnAutoFetch->setText("AutoFetch");
			btnAutoFetch->setCheckable(true);
			btnAutoFetch->setChecked(false);
			toolBar->addWidget(btnAutoFetch);

			QMenu *pMenuViews = new QMenu;

			actionViewsOverview = new QAction(this);
			actionViewsOverview->setText("Overview");
			actionViewsOverview->setCheckable(true);
			pMenuViews->addAction(actionViewsOverview);

			actionViewsSlides = new QAction(this);;
			actionViewsSlides->setText("Slides");
			actionViewsSlides->setCheckable(true);
			pMenuViews->addAction(actionViewsSlides);
			pMenuViews->addSeparator();

			actionViewsPhases = new QAction(this);;
			actionViewsPhases->setText("Phases");
			actionViewsPhases->setCheckable(true);
			pMenuViews->addAction(actionViewsPhases);

			actionViewsContrasts = new QAction(this);;
			actionViewsContrasts->setText("Contrasts");
			actionViewsContrasts->setCheckable(true);
			pMenuViews->addAction(actionViewsContrasts);

			QActionGroup *pActionGroupViews = new QActionGroup(this);
			pActionGroupViews->addAction(actionViewsOverview);
			pActionGroupViews->addAction(actionViewsSlides);
			pActionGroupViews->addAction(actionViewsPhases);
			pActionGroupViews->addAction(actionViewsContrasts);
			actionViewsOverview->setChecked(true);

			QToolButton *btnView = new QToolButton(toolBar);
			btnView->setText("Views");
			btnView->setCheckable(false);
			btnView->setPopupMode(QToolButton::InstantPopup);
			btnView->setMenu(pMenuViews);
			toolBar->addWidget(btnView);

			addToolBar(toolBar);


			//------------------------------------------------------------------
			// Roi Toolbar
			QToolBar *pRoiToolbar = new QToolBar("ROI Toolbar",this);

			QActionGroup *pRoiActionGroup = new QActionGroup(pRoiToolbar);
			pRoiActionGroup->setExclusive(true);

			QAction *pZoom = new QAction(QIcon::fromTheme("input-mouse"),
										 QString("Normal Mode"),
										 pRoiToolbar);
			pZoom->setCheckable(true);
			pZoom->setChecked(true);
			pRoiActionGroup->addAction(pZoom);
			pRoiToolbar->addAction(pZoom);

			QAction *pRect = new QAction(QIcon("res/ico_rect.png"),
										QString("Rectangle"),
										pRoiToolbar);
			pRect->setCheckable(true);
			pRoiActionGroup->addAction(pRect);
			pRoiToolbar->addAction(pRect);

			QAction *pCircle = new QAction(QIcon("res/ico_circle.png"),
											QString("Circle"),
											pRoiToolbar);
			pCircle->setCheckable(true);
			pRoiActionGroup->addAction(pCircle);
			pRoiToolbar->addAction(pCircle);

			QAction *pEllipse = new QAction(QIcon("res/ico_ellipse.png"),
											QString("Ellipse"),
											pRoiToolbar);
			pEllipse->setCheckable(true);
			pRoiActionGroup->addAction(pEllipse);
			pRoiToolbar->addAction(pEllipse);

			QAction *pCircleRing = new QAction(QIcon("res/ico_circlering.png"),
											QString("Circle Ring"),
											pRoiToolbar);
			pCircleRing->setCheckable(true);
			pRoiActionGroup->addAction(pCircleRing);
			pRoiToolbar->addAction(pCircleRing);

			QAction *pCircleSeg = new QAction(QIcon("res/ico_circlesegment.png"),
											QString("Circle Segment"),
											pRoiToolbar);
			pCircleSeg->setCheckable(true);
			pRoiActionGroup->addAction(pCircleSeg);
			pRoiToolbar->addAction(pCircleSeg);

			QAction *pPolygon = new QAction(QIcon("res/ico_polygon.png"),
											QString("Polygon"),
											pRoiToolbar);
			pPolygon->setCheckable(true);
			pRoiActionGroup->addAction(pPolygon);
			pRoiToolbar->addAction(pPolygon);

			pRoiToolbar->addAction(actionClearRoi);

			addToolBar(pRoiToolbar);
			//------------------------------------------------------------------


			//------------------------------------------------------------------
			// Status Bar
			statusbar = new QStatusBar(this);
			pStatusMsg = new QLabel(this);
			pStatusExtCount = new QLabel(this);
			//pStatusMsg->setFrameStyle(QFrame::Panel|QFrame::Sunken);
			statusbar->addWidget(pStatusMsg,1);
			statusbar->addPermanentWidget(pStatusExtCount,0);
			setStatusBar(statusbar);

			ShowRightMessage(0,0,0);
			//------------------------------------------------------------------


			//------------------------------------------------------------------
			// Connections
			// Toolbar
			connect(btnLog, SIGNAL(toggled(bool)),
					this, SLOT(SetLog10(bool)));
			connect(btnAutoFetch, SIGNAL(toggled(bool)),
					this, SLOT(SetAutoFetch(bool)));
			connect(actionViewsOverview, SIGNAL(triggered()),
					this, SLOT(viewOverview()));
			connect(actionViewsSlides, SIGNAL(triggered()),
					this, SLOT(viewSlides()));
			connect(actionViewsPhases, SIGNAL(triggered()),
					this, SLOT(viewPhases()));
			connect(actionViewsContrasts, SIGNAL(triggered()),
					this, SLOT(viewContrasts()));

			// ROI Toolbar
			connect(pZoom, SIGNAL(triggered()), this, SLOT(toolZoom()));
			connect(pRect, SIGNAL(triggered()), this, SLOT(toolRect()));
			connect(pCircle, SIGNAL(triggered()), this, SLOT(toolCircle()));
			connect(pEllipse, SIGNAL(triggered()), this, SLOT(toolEllipse()));
			connect(pCircleRing, SIGNAL(triggered()), this, SLOT(toolCircRing()));
			connect(pCircleSeg, SIGNAL(triggered()), this, SLOT(toolCircSeg()));
			connect(pPolygon, SIGNAL(triggered()), this, SLOT(toolPolygon()));


			// Slider
			connect(sliderFolien, SIGNAL(valueChanged(int)),
					this, SLOT(ChangeFolie(int)));
			connect(sliderZeitkanaele, SIGNAL(valueChanged(int)),
					this, SLOT(ChangeZeitkanal(int)));

			// File
			connect(actionExit, SIGNAL(triggered()), this, SLOT(close()));
			connect(actionBrowseFiles, SIGNAL(triggered()),
					this, SLOT(BrowseFiles()));
			connect(actionLoadPad, SIGNAL(triggered()), this, SLOT(LoadPad()));
			connect(actionLoadPadTxt, SIGNAL(triggered()), this, SLOT(LoadPadTxt()));
			connect(actionLoadTof, SIGNAL(triggered()), this, SLOT(LoadTof()));
			connect(actionSaveFile, SIGNAL(triggered()), this, SLOT(SaveFile()));
			connect(actionSaveDatFile, SIGNAL(triggered()),
					this, SLOT(SaveFileAsDat()));
			connect(actionWriteXML, SIGNAL(triggered()),
					this, SLOT(WriteXML()));
			connect(actionPrint, SIGNAL(triggered()),
					m_cascadewidget.GetPlot(), SLOT(printPlot()));
			connect(actionShowFileParams, SIGNAL(triggered()),
					&m_cascadewidget, SLOT(showFileParams()));

			// Plot
			connect(actionCountRange, SIGNAL(triggered()),
					&m_cascadewidget, SLOT(showRangeDlg()));

			// Server
			connect(actionConnectServer, SIGNAL(triggered()),
					this, SLOT(ConnectToServer()));
			connect(actionServerDisconnect, SIGNAL(triggered()),
					this, SLOT(ServerDisconnect()));

			connect(actionServerCommand, SIGNAL(triggered()),
					this, SLOT(ServerCommand()));

			connect(actionLoadTofServer, SIGNAL(triggered()),
					this, SLOT(LoadTofServer()));
			connect(actionServerMeasurementStart, SIGNAL(triggered()),
					this, SLOT(ServerMeasurementStart()));
			connect(actionServerMeasurementStop, SIGNAL(triggered()),
					this, SLOT(ServerMeasurementStop()));
			connect(actionConfigServer, SIGNAL(triggered()),
					this, SLOT(ServerConfig()));
			connect(actionConfigFromServer, SIGNAL(triggered()),
					this, SLOT(GetServerConfig()));

			// Tools
			connect(actionGenerateRandomPad, SIGNAL(triggered()),
					this, SLOT(GenerateRandomPad()));
			connect(actionGenerateRandomTof, SIGNAL(triggered()),
					this, SLOT(GenerateRandomTof()));
			connect(actionBatchJob, SIGNAL(triggered()),
					this, SLOT(BatchJob()));
			connect(actionPrintLocalConf, SIGNAL(triggered()),
					this, SLOT(PrintLocalConf()));
			connect(actionAreaPhaseCorrect, SIGNAL(triggered()),
					this, SLOT(AreaPhaseCorrect()));

			connect(actionGc, SIGNAL(triggered()),
					this, SLOT(GarbageCollect()));
			connect(actionMem, SIGNAL(triggered()),
					this, SLOT(ShowMemUsage()));


			// Help
			connect(actionAbout, SIGNAL(triggered()),
					this, SLOT(About()));
			connect(actionAboutQt, SIGNAL(triggered()),
					this, SLOT(AboutQt()));

			// Graph
			connect(actionCalibration, SIGNAL(triggered()),
					this, SLOT(showCalibration()));
			connect(actionGraph, SIGNAL(triggered()),
					this, SLOT(showGraph()));
			connect(actionSummen, SIGNAL(triggered()),
					this, SLOT(showSummenDialog()));

			connect(actionIntegrate, SIGNAL(triggered()),
					this, SLOT(showIntegrationDialog()));
			connect(actionCountsVsImages, SIGNAL(triggered()),
					&m_cascadewidget, SLOT(showCountsVsImagesDlg()));
			connect(actionContrastsVsImages, SIGNAL(triggered()),
					&m_cascadewidget, SLOT(showContrastsVsImagesDlg()));

			// Timer
			connect(&m_statustimer, SIGNAL(timeout()),
					this, SLOT(ServerStatus()));

			connect(&m_autofetchtimer, SIGNAL(timeout()),
					this, SLOT(AutoFetch()));

			// Server Message
			connect(&m_client, SIGNAL(MessageSignal(const char*, int)),
					this, SLOT(ServerMessageSlot(const char*, int)));



			// Dir Toolbar
			connect(btnBrowse, SIGNAL(triggered()), this, SLOT(BrowseFiles()));


			// ROI
			connect(actionManageRois, SIGNAL(triggered()),
					this, SLOT(showRoiDlg()));
			connect(actionSaveRoi, SIGNAL(triggered()),
					this, SLOT(SaveRoi()));
			connect(actionLoadRoi, SIGNAL(triggered()),
					this, SLOT(LoadRoi()));
			connect(actionClearRoi, SIGNAL(triggered()),
					this, SLOT(ClearRoi()));

			// Widget
			connect(&m_cascadewidget, SIGNAL(SumDlgSignal(const bool *, int)),
					this, SLOT(FolienSummeSlot(const bool *, int)));
			connect(&m_cascadewidget, SIGNAL(FileHasChanged(const char*)),
					this, SLOT(FileHasChanged(const char*)));
			//------------------------------------------------------------------


			bool bUseAutoFetch = (Config::GetSingleton()->QueryInt(
						"/cascade_config/server/autofetch_use",
						1) !=0 );

			if(bUseAutoFetch)
			{
				btnAutoFetch->setChecked(true);
				SetAutoFetch(true);
			}
		}
};

// Default Values
int MainWindow::NUM_BINS = 100;
int MainWindow::SERVER_STATUS_POLL_TIME = 500;
int MainWindow::AUTOFETCH_POLL_TIME = 250;


int main(int argc, char **argv)
{
	logger.SetCurLogLevel(LOGLEVEL_INFO);
	logger << "This is Cascade Viewer " << CASCADE_VIEVER_VERSION << ".\n\n";
	
	int iRet = -1;
	try
	{
		QApplication a(argc, argv);
		QSettings settings("tobis_stuff", "cascade_viewer");

		setlocale(LC_ALL, "C");
		QLocale::setDefault(QLocale::English);

		bool bConfigOk;
		// Konfigurationssingleton erzeugen
		const char pcConfigFile[] = "./cascade.xml";
		if(!Config::GetSingleton()->Load(pcConfigFile))
		{
			QString strMsg("Configuration file \"%1\" could not be found.\n"
						   "Using default configuration.");
			strMsg = strMsg.arg(pcConfigFile);
			
			QMessageBox::warning(0, "Warning", strMsg, QMessageBox::Ok);

			bConfigOk = false;
		}
		else
		{
			bConfigOk = true;
		}

		// Konfigurationseinstellungen laden
		GlobalConfig::Init();

		if(bConfigOk)
		{
			logger.SetCurLogLevel(LOGLEVEL_INFO);
			logger << "Main: Using configuration in \"" << pcConfigFile << "\".\n";
		}
		else
		{
			logger.SetCurLogLevel(LOGLEVEL_WARN);
			logger << "Main: Using default configuration.\n";
		}

		MainWindow::NUM_BINS = Config::GetSingleton()->QueryInt(
							"/cascade_config/graphs/bin_count",
							MainWindow::NUM_BINS);

		MainWindow::SERVER_STATUS_POLL_TIME = Config::GetSingleton()->QueryInt(
							"/cascade_config/server/status_poll_time",
							MainWindow::SERVER_STATUS_POLL_TIME);

		MainWindow::AUTOFETCH_POLL_TIME	= Config::GetSingleton()->QueryInt(
							"/cascade_config/server/autofetch_poll_time",
							MainWindow::AUTOFETCH_POLL_TIME);

		MainWindow mainWindow;
		mainWindow.resize(900,700);
		mainWindow.restoreGeometry(settings.value("main/geo").toByteArray());
		mainWindow.show();


		QString strBaseDir = GlobalConfig::GetExpConfig().GetBaseDir().c_str();
		QDir dirBase(strBaseDir);
		if(dirBase.exists())
			GlobalConfig::SetCurDir(strBaseDir.toAscii().data());

		QString strDir = settings.value("dirs/last_dir",
								QString(GlobalConfig::GetCurDir().c_str()))
									.toString();
		GlobalConfig::SetCurDir(strDir.toAscii().data());

		// user wants to open file/dir
		if(argc>1)
		{
			QString strArg = argv[1];
			strArg = strArg.trimmed();

			// check if a directory of that name exists
			QDir dir(strArg);
			if(dir.exists())
			{
				GlobalConfig::SetCurDir(strArg.toAscii().data());
				mainWindow.BrowseFiles();
			}
			else
			{
				// check if a file of that name exists
				QFile file(strArg);
				if(file.exists())
					mainWindow.m_cascadewidget.LoadFile(strArg.toAscii().data());
			}
		}

		iRet = a.exec();

		// save settings
		QString strLastDir(GlobalConfig::GetCurDir().c_str());
		settings.setValue("dirs/last_dir", strLastDir);
		settings.setValue("main/geo", mainWindow.saveGeometry());

		// aufräumen
		GlobalConfig::Deinit();
		Config::ClearSingleton();
	}
	catch(std::exception& ex)
	{
		std::cerr << "\n*** GURU MEDITATION ***: " << ex.what() << std::endl;
	}

	return iRet;
}

#ifdef __CASCADE_QT_CLIENT__
	// Qt-Metaobjekte
	#include "cascade.moc"
#endif
