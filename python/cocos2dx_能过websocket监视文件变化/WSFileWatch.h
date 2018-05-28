#pragma once

#include "network/WebSocket.h" //WebSocket头文件路径  
#include "network/CCDownloader.h"

class WSFileWatch:
	public cocos2d::network::WebSocket::Delegate {
public:
	WSFileWatch();
	void init(const char* fileWathAddress, const char* downLoadAddress);
	//这些虚函数WebSocket的回调  
	virtual void onOpen(cocos2d::network::WebSocket* ws);
	virtual void onMessage(cocos2d::network::WebSocket* ws, const cocos2d::network::WebSocket::Data& data);
	virtual void onClose(cocos2d::network::WebSocket* ws);
	virtual void onError(cocos2d::network::WebSocket* ws, const cocos2d::network::WebSocket::ErrorCode& error);
private:
	void changeFile(std::string data);
	void downloadfile(std::string url, std::string savepath);
	void checkAtStart();
private:
	cocos2d::network::Downloader* mDownloader;
	//WebSocket实例化  
	cocos2d::network::WebSocket* m_pWebSocket;
	std::string mStaticFileUrl;
	std::string mSavePath;
};