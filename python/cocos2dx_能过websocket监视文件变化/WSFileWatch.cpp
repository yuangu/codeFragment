#include "WSFileWatch.h"
#include "json/document-wrapper.h"
#include "cocos2d.h"
#include "network/HttpClient.h"  

USING_NS_CC;
struct FileEvent
{
	std::string event;
	std::string src_path;
	std::string dest_path;
	bool is_directory;
};


using namespace cocos2d::network;


WSFileWatch::WSFileWatch()
{
	mDownloader = new cocos2d::network::Downloader();

	// 下载失败
	mDownloader->onTaskError = [this](const cocos2d::network::DownloadTask& task,
		int errorCode,
		int /*errorCodeInternal*/,
		const std::string& /*errorStr*/)
	{
		CCLOG("onTaskError");
	};

	// 进度回掉
	mDownloader->onTaskProgress = [this](const cocos2d::network::DownloadTask& task,
		int64_t /*bytesReceived*/,
		int64_t totalBytesReceived,
		int64_t totalBytesExpected)
	{
		int percent = totalBytesExpected ? int(totalBytesReceived * 100 / totalBytesExpected) : 0;
		CCLOG("downloading... %d%%", percent);		
	};

	// get version from version file when get data success
	mDownloader->onDataTaskSuccess = [this](const cocos2d::network::DownloadTask& /*task*/,
		std::vector<unsigned char>& data)
	{
		CCLOG("onTaskError");
	};

	//下载完成
	mDownloader->onFileTaskSuccess = [this](const cocos2d::network::DownloadTask& task)
	{
		CCLOG("onFileTaskSuccess");
		
	};

	mSavePath = CCFileUtils::getInstance()->getWritablePath() + "update/";	
}



void WSFileWatch::init(const char* fileWathAddress, const char* downLoadAddress)
{
	m_pWebSocket = new WebSocket();
	m_pWebSocket->init(*this, fileWathAddress);//实例化WebSocket并连接
	mStaticFileUrl = downLoadAddress; 

	checkAtStart();
}

void WSFileWatch::onOpen(WebSocket * ws)
{
	CCLOG("OnOpen");
}

void  WSFileWatch::onMessage(WebSocket * ws, const WebSocket::Data & data)
{
	changeFile(data.bytes);
	
	CCLOG(data.bytes);
}

void WSFileWatch::onClose(WebSocket * ws)
{
	if (ws == m_pWebSocket)
	{
		m_pWebSocket = NULL;
	}
	CC_SAFE_DELETE(ws);
	CCLOG("onClose");
}

void WSFileWatch::onError(WebSocket * ws, const WebSocket::ErrorCode & error)
{
	if (ws == m_pWebSocket)
	{
		char buf[100] = { 0 };
		sprintf(buf, "an error was fired, code: %d", error);
	}
	CCLOG("Error was fired, error code: %d", error);
}

void WSFileWatch::changeFile(std::string data)
{
	rapidjson::Document document;
	document.Parse<0>(data.c_str());

	FileEvent fileEvent;

	//是不是文件夹
	if (document.HasMember("is_directory"))
	{
		rapidjson::Value& is_directory = document["is_directory"];
		fileEvent.is_directory = is_directory.GetBool();
	}
	else
	{
		return;
	}

	if (document.HasMember("src_path"))
	{
		rapidjson::Value& src_path = document["src_path"];
		fileEvent.src_path.append(src_path.GetString(), src_path.GetStringLength());
	}
	else
	{
		return;
	}

	if (document.HasMember("event"))
	{
		rapidjson::Value& event = document["event"];
		fileEvent.event.append(event.GetString(), event.GetStringLength());
	}
	else
	{
		return;
	}

	if (document.HasMember("dest_path"))
	{
		rapidjson::Value& dest_path = document["dest_path"];
		fileEvent.dest_path.append(dest_path.GetString(), dest_path.GetStringLength());
	}

	
	if (fileEvent.event == "created" || fileEvent.event == "modified")
	{
		if (!fileEvent.is_directory)
		{
			downloadfile(mStaticFileUrl + fileEvent.src_path, mSavePath + fileEvent.src_path);
		}
		else {
			if (!CCFileUtils::getInstance()->isDirectoryExist(mSavePath + fileEvent.src_path))
			{
				CCFileUtils::getInstance()->createDirectory(mSavePath + fileEvent.src_path);
			}
		}
	}
	else if (fileEvent.event == "moved")
	{
		if (!fileEvent.is_directory)
		{
			if (!CCFileUtils::getInstance()->isFileExist(mSavePath + fileEvent.src_path))
			{
				downloadfile(mStaticFileUrl + fileEvent.dest_path, mSavePath + fileEvent.dest_path);
			}
			else {
				CCFileUtils::getInstance()->renameFile(mSavePath + fileEvent.src_path, mSavePath + fileEvent.dest_path);
			}
		}
		else {
			if (CCFileUtils::getInstance()->isDirectoryExist(mSavePath + fileEvent.src_path))
			{
				CCFileUtils::getInstance()->renameFile(mSavePath + fileEvent.src_path, mSavePath + fileEvent.dest_path);
			}
		}
	}
	else if (fileEvent.event == "deleted")
	{
		if (!fileEvent.is_directory)
		{
			if (CCFileUtils::getInstance()->isFileExist(mSavePath + fileEvent.src_path))
			{
				CCFileUtils::getInstance()->removeFile(mSavePath + fileEvent.src_path);
			}			
		}
		else
		{
			if (CCFileUtils::getInstance()->isDirectoryExist(mSavePath + fileEvent.src_path))
			{
				CCFileUtils::getInstance()->removeDirectory(mSavePath + fileEvent.src_path);
			}
		}
	}

}

void WSFileWatch::downloadfile(std::string url, std::string savepath)
{
	if (CCFileUtils::getInstance()->isFileExist(savepath))
	{
		CCFileUtils::getInstance()->removeFile(savepath);
	}

	auto task = mDownloader->createDownloadFileTask(url, savepath);
	
}

//启动时候做文件效正检查
void WSFileWatch::checkAtStart()
{
	HttpRequest* request = new (std::nothrow) HttpRequest();	
	request->setUrl(mStaticFileUrl + "version.json");
	// 设置请求类型，可以选择GET  
	request->setRequestType(HttpRequest::Type::GET);
	// 设置请求完成之后的响应方法  
	request->setResponseCallback([=](HttpClient* client, HttpResponse* response) {
		std::vector<char>* data = response->getResponseData();
		rapidjson::Document document;
		std::string buff;
		buff.append((const char*)&((*data)[0]), data->size());
		document.Parse<0>(buff.c_str());

		for (auto iter = document.MemberBegin(); iter != document.MemberEnd(); ++iter)
		{
			auto key = (iter->name).GetString();
			auto& v = document[key];
			auto md5 = v["md5"].GetString();
			auto size = v["size"].GetInt64();
			auto path = v["path"].GetString();

			if (utils::getFileMD5Hash(mSavePath + path) != md5)
			{
				downloadfile(mStaticFileUrl + path, mSavePath + path);
			}

		}
	});
	HttpClient::getInstance()->send(request);
	request->release();
}