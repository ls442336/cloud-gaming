#pragma once

#include <winsock2.h>
#include <iostream>

#pragma comment(lib,"ws2_32.lib")

class ScreenRecorderClient {
public:
	SOCKET sock;
	struct sockaddr_in server;
	int id;

	std::string address;
	int port;

	ScreenRecorderClient(std::string address, int port);
	int Init();
	bool Send(char* data, int size);
};