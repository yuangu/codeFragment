#pragma once

#include "network/WebSocket.h" //WebSocketͷ�ļ�·��  
#include "network/CCDownloader.h"

class WSFileWatch:
	public cocos2d::network::WebSocket::Delegate {
public:
	WSFileWatch();
	void init(const char* fileWathAddress, const char* downLoadAddress);
	//��Щ�麯��WebSocket�Ļص�  
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
	//WebSocketʵ����  
	cocos2d::network::WebSocket* m_pWebSocket;
	std::string mStaticFileUrl;
	std::string mSavePath;
};