// *****************************************************************************
// NICOS, the Networked Instrument Control System of the FRM-II
// Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
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
// Klassen zum Laden und Verarbeiten von Tof-Dateien

#ifndef __TOFLOADER__
#define __TOFLOADER__

#include "../config/globals.h"
#include "../auxiliary/roi.h"
#include "basicimage.h"
#include "padloader.h"
#include "conf.h"

class TmpImage;
class TmpGraph;
class TofImage;
class PadImage;


//==============================================================================

/**
 * \brief class for temporary images generated by some methods of the
 * TofImage class
 */
class TmpImage : public BasicImage
{
	friend class PadImage;
	friend class TofImage;

  protected:
	/// image dimensions
	int m_iW, m_iH;

	//--------------------------------------------------------------------------
	// only one of the following pointers is actually used (the other has
	// to be NULL)

	/// pointer to array for counts data
	unsigned int* m_puiDaten;
	/// pointer to array for contrast/phase data
	double* m_pdDaten;
	//--------------------------------------------------------------------------

	/// lower & upper bound values
	double m_dMin, m_dMax;
	/// position of maximum
	Vec2d<int> m_vecMax;

	TofConfig m_TofConfig;

	const Vec2d<int>& GetMaxCoord() const;

  public:
	/// create EMPTY TmpImage without allocating any memory etc.
	/// (which is done externally)
	TmpImage(const TofConfig* pTofConf=0);

	/// create TmpImage from other TmpImage; does NOT allocate memory
	TmpImage(const TmpImage& tmp);
	TmpImage& operator=(const TmpImage& tmp);

	virtual ~TmpImage();

	/// clean up
	void Clear(void);

	/// get data point (if "wrong" type is requested, the return value is cast)
	virtual double GetData(int iX, int iY) const;
	virtual unsigned int GetIntData(int iX, int iY) const;
	virtual double GetDoubleData(int iX, int iY) const;

	virtual int GetWidth() const;
	virtual int GetHeight() const;

	/// calculate lower & upper bound values
	void UpdateRange();

	virtual int GetIntMin(void) const;
	virtual int GetIntMax(void) const;
	virtual double GetDoubleMin(void) const;
	virtual double GetDoubleMax(void) const;

	/// write XML representation of image
	bool WriteXML(const char* pcFileName,
				  int iSampleDetector=0,
				  double dWavelength=0,
				  double dLifetime=0,
				  int iBeamMonitor=0) const;

	/// create TmpImage from PAD image
	void ConvertPAD(PadImage* pPad);

	/// adds another TmpImage to this one
	void Add(const TmpImage& tmp);

	/// Gaussian fit for finding the beam center
	bool FitGaussian(double &dAmp,
					 double &dCenterX, double &dCenterY,
					 double &dSpreadX, double &dSpreadY) const;

	TmpGraph GetRadialIntegration(double dAngleInc, double dRadInc,
								  const Vec2d<double>& vecCenter,
								  bool bAngMean) const;
};


//==============================================================================

/**
 * \brief class for temporary graph data generated by some methods of the
 * 			TofImage class
 */
class TmpGraph
{
  friend class TofImage;
  friend class TmpImage;

  protected:
	/// # of data points
	int m_iW;

	/// pointer to data array
	unsigned int* m_puiDaten;

	TofConfig m_TofConfig;

  public:
	/// create empty graph (does not allocate memory)
	TmpGraph(const TofConfig* pTofConf=0);
	virtual ~TmpGraph();

	/// create TmpGraph from other TmpGraph; does NOT allocate memory
	TmpGraph(const TmpGraph& tmp);
	TmpGraph& operator=(const TmpGraph& tmp);

	/// fit a sinus function to the data points
	/// \return fit successful?
	bool FitSinus(double& dFreq, double &dPhase, double &dAmp, double &dOffs,
				  double &dPhase_err, double &dAmp_err, double &dOffs_err) const;
	bool FitSinus(double& dFreq, double &dPhase, double &dAmp, double &dOffs) const;

	bool GetContrast(double &dContrast, double &dPhase,
					double &dContrast_err, double &dPhase_err,
					const TmpGraph* punderground=0, double dMult_ug=0) const;
	bool GetContrast(double &dContrast, double &dPhase) const;

	static bool CalcContrast(double dAmp, double dOffs,
						double dAmp_err, double dOffs_err,
						double &dContrast, double &dContrast_err);

	bool Save(const char* pcFile) const;

	//--------------------------------------------------------------------------
	// getter
	unsigned int GetData(int iX) const;
	int GetWidth(void) const;
	int GetMin() const;
	int GetMax() const;
	//--------------------------------------------------------------------------

	/// is sum of data points < iTotal?
	bool IsLowerThan(unsigned int iTotal) const;

	unsigned int Sum(void) const;
};


//==============================================================================

/**
 * \brief container representing a TOF image
 * 
 * corresponds to the "TOF" measurement type in the server & HardwareLib
 */
class TofImage : public Countable
{
	protected:
		/// pointer to data array (format depends on compression used)
		unsigned int *m_puiDaten;

		/// TOF data stored in external memory which needs no management,
		/// i.e. allocation & freeing?
		bool m_bExternalMem;

		TofConfig m_config;

		Roi m_roi;
		bool m_bUseRoi;
		bool m_bOk;

		CascConf m_cascconf;

	public:
		const TofConfig& GetTofConfig() const;
		const CascConf& GetLocalConfig() const;

		virtual Roi& GetRoi();
		virtual void UseRoi(bool bUseRoi=true);
		virtual bool GetUseRoi() const;

		TofImage(const char *pcFileName=NULL,
				 bool bExternalMem=false, const TofConfig* conf=0);

		virtual ~TofImage();

		TofImage *copy() const;

		/// set pointer to external memory (if bExternalMem==true)
		void SetExternalMem(void* pvDaten);

		int GetTofSize() const;
		void Clear();

		/// get specific count value
		unsigned int GetData(int iFoil, int iTimechannel, int iX, int iY) const;
		unsigned int GetData(int iImage, int iX, int iY) const;

		/// set specific count value
		void SetData(int iImage, int iX, int iY, unsigned int uiCnt);
		void SetData(int iFoil, int iTc, int iX, int iY, unsigned int uiCnt);

		/// same as above, but return 0 if outside ROI (if ROI is used)
		unsigned int GetDataInsideROI(int iFoil, int iTimechannel,
									  int iX, int iY) const;
		unsigned int GetDataInsideROI(int iImage, int iX, int iY) const;

		/// get raw pointer to data array
		unsigned int* GetRawData(void) const;

		int LoadFile(const char *pcFileName);
		int SaveFile(const char *pcFileName);

		/// \param strBufLen: number of bytes
		int LoadMem(const char *strBuf, unsigned int strBufLen);

		/// total number of counts (inside ROI, if used)
		virtual unsigned int GetCounts() const;
		virtual unsigned int GetCountsSubtractBackground() const;
		unsigned int GetCounts(int iFoil) const;

		/// \deprecated old style GetCounts, ignoring main roi
		unsigned int GetCounts(int iStartX, int iEndX,
							   int iStartY, int iEndY) const;

		//----------------------------------------------------------------------
		/// copy ROI into new temporary image
		/// \todo: rename method to avoid confusion with new ROI stuff
		TmpImage GetROI(int iStartX, int iEndX, int iStartY, int iEndY,
						int iFoil, int iTimechannel) const;

		/// get graph for counts vs. time channels
		TmpGraph GetGraph(int iStartX, int iEndX, int iStartY, int iEndY,
						  int iFoil, bool bIgnoreRoi=false) const;

		TmpGraph GetGraph(int iFoil) const;

		/// phase-shifted addition of all foils
		TmpGraph GetTotalGraph(int iStartX, int iEndX, int iStartY, int iEndY) const;
		TmpGraph GetTotalGraph() const;

		/// get overview image (summing all individual images in TOF)
		TmpImage GetOverview(bool bOnlyInRoi=false) const;

		TmpImage GetFoil(int iFoil, bool bOnlyInRoi=false) const;

		/// phase image
		TmpImage GetPhaseGraph(int iFoil, bool bInDeg=true) const;

		/// contrast image
		TmpImage GetContrastGraph(int iFoil) const;

		/// sum foils/phases/contrasts marked in respective bool array
		TmpImage AddFoils(const bool *pbChannels) const;
		TmpImage AddPhases(const bool *pbFoils) const;
		TmpImage AddContrasts(const bool *pbFoils) const;

		void AddFoils(int iBits, int iChannelBits, TmpImage *pImg) const;
		//----------------------------------------------------------------------

		/// generate a random TOF image for testing
		void GenerateRandomData();

		/// subtract another tof from this
		void Subtract(const TofImage& tof, double dTimes=1.);

		bool IsOk() const;

		bool SaveAsDat(const char* pcDat, int iSelFoil=-1) const;
		bool SaveTcs(const char* pcDat) const;

		bool AreaPhaseCorrect();
};

#endif
