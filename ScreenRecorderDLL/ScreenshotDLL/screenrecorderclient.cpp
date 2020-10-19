#include "screenrecorderclient.h"

#include <sstream>
#include "easylogging++.h"

ScreenRecorderClient::ScreenRecorderClient(
	std::string address,
	int port
)
	:	address(address),
		port(port)
{

}

int ScreenRecorderClient::Init()
{
	id = 0;

	WSADATA wsa;

	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	{
		return 1;
	}

	if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) == INVALID_SOCKET)
	{
		return 2;
	}

	server.sin_addr.s_addr = inet_addr(address.c_str());
	server.sin_family = AF_INET;
	server.sin_port = htons(port);

	return 0;
}

unsigned char* intToByte(const int& N) {

	unsigned char* byte = new unsigned char[4];

	byte[0] = (N >> 24) & 0xFF;
	byte[1] = (N >> 16) & 0xFF;
	byte[2] = (N >> 8) & 0xFF;
	byte[3] = N & 0xFF;

	return byte;
}

bool ScreenRecorderClient::Send(
	char* data,
	int size
)
{
	data[size] = (id >> 24) & 0xFF;
	data[size + 1] = (id >> 16) & 0xFF;
	data[size + 2] = (id >> 8) & 0xFF;
	data[size + 3] = id & 0xFF;

	sendto(sock, data, size + 4, 0, (const struct sockaddr*) &server, sizeof(server));

	id++;

	return true;
}