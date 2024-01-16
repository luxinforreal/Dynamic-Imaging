#ifndef FL_DLP_HS_H
#define FL_DLP_HS_H

// # define FL_DLP_HS_API extern "C" __declspec(dllexport)
# define FL_DLP_HS_API __declspec(dllexport)

#include <stdio.h>
#include <winsock2.h>
#include <windows.h>
#include <time.h>
#include <math.h>
#include <dirent.h>

//----------------------------------------------------------------

#define FL_DLP_HS_LENGTH_CMD 4     //The Length of CMD_HEAD  4byte
#define FL_DLP_HS_LENGTH_HEAD 4    //The Length of HEAD      4byte

#define FL_DLP_HS_FLAG_HEAD1    0xF5    //HEAD1
#define FL_DLP_HS_FLAG_HEAD2    0xFF    //HEAD2

#define FL_DLP_HS_FORMAT_FLAG_PARAM_QUERY 0x80 //Query Command Header


/// @brief: resolution type
typedef int FL_DLP_HS_RESOLUTION_TYPE_CODE;
enum FL_DLP_HS_RESOLUTION_TYPE {
    FL_DLP_HS_RES_NULL,
    FL_DLP_HS_RES_095_1080P,  // 0.95 1080p    1920*1080
    FL_DLP_HS_RES_070_XGA,    // 0.7  XGA      1024*768
    FL_DLP_HS_RES_055_XGA,    // 0.55 XGA      1024*768
    FL_DLP_HS_RES_096_WUXGA,  // 0.96  WUXGA   1920*1200
    FL_DLP_HS_RES_065_WXGA,   // 0.65  WXGA    1280*800
    FL_DLP_HS_RES_065_1080P,  // 0.65  1080P   1920*1080
    FL_DLP_HS_RES_090_WQXGA   // 0.9   WQXGA   2560*1600
};

///@brief:Device Info
typedef struct {

    unsigned int picnum_1bit ;                //pic num of 1 bit
    unsigned int picnum_8bit ;                //pic num of 8 bit

    unsigned int delaytime;                   //Delay parameters

    bool DDR1;                                //DDR1 init state
    bool DDR2;                                //DDR2 init state

    FL_DLP_HS_RESOLUTION_TYPE_CODE resolution;   //[use]resolving power

    unsigned long long Address_add;           //[use]Address increment 1 pic

} FL_DLP_HS_Dev_Info;

///@brief:Device
typedef struct{

    int DeviceID;                        //ID

    SOCKET rece_socket;                  //UDP socket

    SOCKADDR_IN udp_Up_ctx;              //Upper computer
    SOCKADDR_IN udp_Down_ctx;            //Lower machine

    FL_DLP_HS_Dev_Info DeviceInfo;       //Device Info

}FL_DLP_HS_Device;

///@brief: CMD_TYPE
typedef int FL_DLP_HS_CMD_TYPE_CODE;
enum FL_DLP_HS_UDP_CMD_TYPE {
    FL_DLP_HS_CMD_LOAD_IMAGE = 0,         // load image
    FL_DLP_HS_CMD_INTER_PLAY_SINGLE,      // internal single play
    FL_DLP_HS_CMD_INTER_PLAY_LOOP,        // internal loop play
    FL_DLP_HS_CMD_EXTER_PLAY_SINGLE,      // exter single play
    FL_DLP_HS_CMD_EXTER_PLAY_LOOP,        // exter loop play
    FL_DLP_HS_CMD_PLAY_PAUSE,             // play pause
    FL_DLP_HS_CMD_SET_PARAM,              // set parameter
    FL_DLP_HS_CMD_QUERY,                  // query
    FL_DLP_HS_CMD_PLAY_STOP,              // play stop

    FL_DLP_HS_CMD_DLP_FLOAT,              // dlp_float
    FL_DLP_HS_CMD_DLP_RST,                // dlp_reset
    FL_DLP_HS_CMD_DLP_UPDOWN,             // Upside down
    FL_DLP_HS_CMD_DLP_REVERSE,            // Reverse
    FL_DLP_HS_CMD_DLP_SoftTRI,            // Software trigger

    FL_DLP_HS_CMD_VS_INTER_PLAY_SINGLE,   // Variable sequence internal single play
    FL_DLP_HS_CMD_VS_INTER_PLAY_LOOP,     // Variable sequence internal loop play
    FL_DLP_HS_CMD_VS_EXTER_PLAY_SINGLE,   // Variable sequence exter single play
    FL_DLP_HS_CMD_VS_EXTER_PLAY_LOOP,     // Variable sequence exter loop play

    FL_DLP_HS_CMD_SETVS,                  // set Variable sequence

    FL_DLP_HS_CMD_MAX,                    //
};

/// @brief: CMD_HEAD array
const unsigned char FL_DLP_HS_Fix_Cmd_Array[50] = {
    0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70,
    0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0,
    0x20, 0x30, 0x40, 0x50, 0xFF
 };



///@brief: RESULT CODE
typedef int FL_DLP_HS_RESULT_CODE;
enum FL_DLP_HS_RESULT_TYPE{
    FL_DLP_HS_RESULT_SUCCESS = 0,      // SUCCESS

};

///@brief:ERROR CODE
enum FL_DLP_HS_RESULT_ERR_TYPE {
    FL_DLP_HS_RESULT_ERR_socketCreateFail = -100,
    FL_DLP_HS_RESULT_ERR_socketBindFail,
    FL_DLP_HS_RESULT_ERR_NoParam_CMDTypeError,
    FL_DLP_HS_RESULT_ERR_SendFail,
    FL_DLP_HS_RESULT_ERR_DataisnotQueryCMD,
    FL_DLP_HS_RESULT_ERR_CMD_Param_GrayError,
    FL_DLP_HS_RESULT_ERR_CMD_Param_DelayError,
    FL_DLP_HS_RESULT_ERR_CMD_Param_InverseError,
    FL_DLP_HS_RESULT_ERR_CMD_Param_CFPicnumError,
    FL_DLP_HS_RESULT_ERR_CMD_Param_CFDelayError,
    FL_DLP_HS_RESULT_ERR_CMD_PlayTypeError,
    FL_DLP_HS_RESULT_ERR_CMD_Play_Param_StartPError,
    FL_DLP_HS_RESULT_ERR_CMD_Play_Param_PlayPicnum_StartPError,

    FL_DLP_HS_RESULT_ERR_SendPicError,
    FL_DLP_HS_RESULT_ERR_SendPic1_BMPDirnumXYpicnum,
    FL_DLP_HS_RESULT_ERR_SendPic1_openBMPDirError,
    FL_DLP_HS_RESULT_ERR_SendPicSendtypeError,

    FL_DLP_HS_RESULT_ERR_SendPic2_BMPDirnumXYpicnum,
    FL_DLP_HS_RESULT_ERR_SendPic2_openBMPDirError,

    FL_DLP_HS_RESULT_ERR_SendPic3_openBinError,
    FL_DLP_HS_RESULT_ERR_SendPic3_picnumError,
};

//----------------------------------------------------------------

/// @brief: Initialize the UDP ;Bind host computer IP and port,Enter the IP and port of the lower computer
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE FL_DLP_HS_Init(int DeviceID,char* server_addr,int server_port,char* target_addr,int target_port);

/// @brief: Close UDP
FL_DLP_HS_API void FL_DLP_HS_DeInit(int DeviceID);

/// @brief: Receive UDP Info
FL_DLP_HS_API int FL_DLP_HS_Reveive(int DeviceID,unsigned char *buff);

/// @brief: CMD withnot param(8 CMD)
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE FL_DLP_HS_Send_Fixed_Cmd_Noparam(int DeviceID, FL_DLP_HS_CMD_TYPE_CODE type);

/// @brief: The analysis and query command returns to obtain the device informationa
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE FL_DLP_HS_AnalysisDevice(int DeviceID,unsigned char buff[21],unsigned char *DeviceInfo,int * DeviceInfolen);

/// @brief: CMD-SetParam1(1 CMD)
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE FL_DLP_HS_Send_Cmd_SetParam(int DeviceID,int Param_Delay,int Param_Inverse,int Param_Gray,int Param_CFPicnum,int Param_CFDelay);

/// @brief: CMD Play(8 CMD)
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE FL_DLP_HS_Send_CMD_Play(int DeviceID,FL_DLP_HS_CMD_TYPE_CODE type,int Param_StartP,int Param_PlayPicnum);

/// @brief: CMD Set Play Sequence
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE FL_DLP_HS_Send_CMD_SetPlaySequence(int DeviceID,int Sequence_num,char * Sequence_Add,char * Sequence_Time);

/// @brief: CMD Set Play Sequence
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE M_FL_DLP_HS_Send_CMD_SetPlaySequence(int DeviceID,int Sequence_num,unsigned char * Sequence_Add,unsigned char * Sequence_Time);

/// @brief: CMD SendPic
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE FL_DLP_HS_Send_PICDATA(int DeviceID,int sendpic_type,char * pic_addr,int pic_num,int Param_StartPicPosition,char * PicData);

/// @brief: CMD SendPic
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE M_FL_DLP_HS_Send_PICDATA(int DeviceID,int sendpic_type,char * pic_addr,int pic_num,int Param_StartPicPosition,unsigned char * PicData);

/// @brief: CMD-Custom Commands
FL_DLP_HS_API FL_DLP_HS_RESULT_CODE FL_DLP_HS_Send_Custom_Cmd(int DeviceID, unsigned char* data, int len);

#endif // FL_DLP_HS_H
