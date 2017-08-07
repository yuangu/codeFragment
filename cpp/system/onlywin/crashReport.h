#include <windows.h>
#include <Dbghelp.h>
#include "util/utils.h"
#pragma auto_inline (off)
#pragma comment( lib, "DbgHelp" )

long   __stdcall  CrashCallBack(_EXCEPTION_POINTERS* pExInfo)
{
	 std::string p = Utils::getwd();
	 p =  p + "/dumpfile.dmp";
     HANDLE hFile = ::CreateFileA(p.c_str(), GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
     if( hFile != INVALID_HANDLE_VALUE)
     {
         MINIDUMP_EXCEPTION_INFORMATION einfo;
         einfo.ThreadId = ::GetCurrentThreadId();
         einfo.ExceptionPointers = pExInfo;
         einfo.ClientPointers = FALSE;
        ::MiniDumpWriteDump(::GetCurrentProcess(), ::GetCurrentProcessId(), hFile, MiniDumpNormal, &einfo, NULL, NULL);
        ::CloseHandle(hFile);
     }
    return 1;
}

void setCrashReport()
{
      SetUnhandledExceptionFilter(CrashCallBack);
}
