#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
#include <mutex>
#include <Indicium/Engine/IndiciumCore.h>
#include <Indicium/Engine/IndiciumDirect3D9.h>
#include <iostream>
#include <sstream>
#include <chrono>
#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>

#include "INIReader.h"
#include "screenrecorderclient.h"

using namespace cv;

EVT_INDICIUM_GAME_HOOKED EvtIndiciumGameHooked;
EVT_INDICIUM_GAME_UNHOOKED EvtIndiciumGameUnhooked;

EVT_INDICIUM_D3D9_PRESENT EvtIndiciumD3D9Present;
EVT_INDICIUM_D3D9_RESET EvtIndiciumD3D9Reset;

ScreenRecorderClient* screenRecorderClient = nullptr;

BOOL WINAPI DllMain(HINSTANCE hInstance, DWORD dwReason, LPVOID)
{
	DisableThreadLibraryCalls(static_cast<HMODULE>(hInstance));

	INDICIUM_ENGINE_CONFIG cfg;
	INDICIUM_ENGINE_CONFIG_INIT(&cfg);

	cfg.Direct3D.HookDirect3D9 = TRUE;
	cfg.EvtIndiciumGameHooked = EvtIndiciumGameHooked;

	switch (dwReason)
	{
	case DLL_PROCESS_ATTACH:
		(void)IndiciumEngineCreate(
			static_cast<HMODULE>(hInstance),
			&cfg,
			NULL
		);

		break;
	case DLL_PROCESS_DETACH:
		(void)IndiciumEngineDestroy(static_cast<HMODULE>(hInstance));

		break;
	default:
		break;
	}

	return TRUE;
}

void EvtIndiciumGameHooked(
	PINDICIUM_ENGINE EngineHandle,
	const INDICIUM_D3D_VERSION GameVersion
)
{
	// Load configs
	INIReader reader("config.ini");

	if (reader.ParseError() != 0) {
		MessageBox(NULL, L"Can't load 'config.ini'", L"ScreenRecorderClient Error", MB_OK);
	}
	
	std::string address = reader.Get("server", "address", "UNKNOWN");
	int port = reader.GetInteger("server", "port", -1);

	screenRecorderClient = new ScreenRecorderClient(address, port);
	screenRecorderClient->Init();

	INDICIUM_D3D9_EVENT_CALLBACKS d3d9;
	INDICIUM_D3D9_EVENT_CALLBACKS_INIT(&d3d9);

	d3d9.EvtIndiciumD3D9PostPresent = EvtIndiciumD3D9Present;
	d3d9.EvtIndiciumD3D9PreReset = EvtIndiciumD3D9Reset;

	switch (GameVersion)
	{
	case IndiciumDirect3DVersion9:
		IndiciumEngineSetD3D9EventCallbacks(EngineHandle, &d3d9);
		break;
	}
}

void EvtIndiciumGameUnhooked()
{
#ifdef WNDPROC_HOOK
	auto& logger = Logger::get(__func__);

	if (MH_DisableHook(MH_ALL_HOOKS) != MH_OK)
	{
		logger.fatal("Couldn't disable hooks, host process might crash");
		return;
	}

	IndiciumEngineLogInfo("Hooks disabled");

	if (MH_Uninitialize() != MH_OK)
	{
		logger.fatal("Couldn't shut down hook engine, host process might crash");
		return;
	}
#endif
}

#pragma region D3D9(Ex)

void EvtIndiciumD3D9Present(
	LPDIRECT3DDEVICE9   pDevice,
	const RECT* pSourceRect,
	const RECT* pDestRect,
	HWND                hDestWindowOverride,
	const RGNDATA* pDirtyRegion
)
{
	static auto initialized = false;
	static bool show_overlay = true;
	static std::once_flag init;

	std::call_once(init, [&](LPDIRECT3DDEVICE9 pd3dDevice)
		{
			D3DDEVICE_CREATION_PARAMETERS params;

			const auto hr = pd3dDevice->GetCreationParameters(&params);
			if (FAILED(hr))
			{
				IndiciumEngineLogError("Couldn't get creation parameters from device");
				return;
			}

			IDirect3DSwapChain9* swapChain;
			pd3dDevice->GetSwapChain(0, &swapChain);

			if (swapChain) {
				D3DPRESENT_PARAMETERS params;
				swapChain->GetPresentParameters(&params);

				params.Flags = params.Flags | D3DPRESENTFLAG_LOCKABLE_BACKBUFFER;

				pd3dDevice->Reset(&params);
			}

			initialized = true;

		}, pDevice);

	if (!initialized)
		return;

	IDirect3DSurface9* surface;
	D3DDISPLAYMODE mode;

	D3DDEVICE_CREATION_PARAMETERS cparams;
	RECT rect;

	pDevice->GetCreationParameters(&cparams);
	GetClientRect(cparams.hFocusWindow, &rect);

	UINT width = rect.right;
	UINT height = rect.bottom;

	D3DLOCKED_RECT rc;

	LPBYTE buffer = new BYTE[4 * width * height];

	HRESULT result = pDevice->GetBackBuffer(0, 0, D3DBACKBUFFER_TYPE_MONO, &surface);

	if(result == D3D_OK){
		surface->LockRect(&rc, NULL, 0);
		CopyMemory(buffer, rc.pBits, 4 * width * height);
		surface->UnlockRect();

		Mat imageMat(height, width, CV_8UC4, buffer);

		std::vector<unsigned char> encodedImage;

		std::vector<int> compression_params;	
		compression_params.push_back(IMWRITE_JPEG_QUALITY);
		compression_params.push_back(30);

		imencode(".jpg", imageMat, encodedImage, compression_params);

		for(int i = 0; i < 4; i++)
			encodedImage.push_back(0);

		screenRecorderClient->Send((char *) ((encodedImage).data()), encodedImage.size());
	}

	if (surface) {
		surface->Release();
	}

	delete[] buffer;
}

void EvtIndiciumD3D9Reset(
	LPDIRECT3DDEVICE9       pDevice,
	D3DPRESENT_PARAMETERS* pPresentationParameters
)
{
	pPresentationParameters->Flags = pPresentationParameters->Flags | D3DPRESENTFLAG_LOCKABLE_BACKBUFFER;
}
#pragma endregion