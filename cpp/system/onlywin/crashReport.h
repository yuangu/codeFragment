#include <windows.h>
#include <Dbghelp.h>
#include <direct.h>
#include <time.h>
#pragma auto_inline (off)
#pragma comment( lib, "DbgHelp" )

long __stdcall  CrashCallBack(_EXCEPTION_POINTERS* pExInfo)
{
	 char buffer[_MAX_PATH] = {0x00};
	 getcwd(buffer, _MAX_PATH);
	 std::string p = buffer;
	 std::cout << p << std::endl;

	 //获取以时间为准 
	 time_t lt = time(NULL);
	 struct tm* t = localtime(&lt);
	 memset(buffer, 0, _MAX_PATH);
	 sprintf(buffer, "/dumpfile_%04d-%02d-%02d_%02d-%02d-%02d.dmp", 1900 + t->tm_year, t->tm_mon + 1, t->tm_mday, t->tm_hour, t->tm_min, t->tm_sec);

	 p =  p + buffer;
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
