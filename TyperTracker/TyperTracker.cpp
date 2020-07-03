#include "pch.h"
#include <iostream>
#include <ctime>
#include <string>
#include <fstream>
#include <Windows.h>

/*
Typer Tracker
Created by Allison Quinlan
Started May 2020
*/

using namespace std;

HHOOK mouseHook;
HHOOK keyHook;
std::string base = "C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\";
int dataCount = 0;

/* Periodically calls python code to upload to SQL*/
void uploadData() {
	dataCount++;
	if (dataCount > 1000) {
		//WinExec("pythonw C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\upload.py", SW_HIDE);
		system("python C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\upload.py");
		dataCount = 0;
	}
}

/* Adds current time in 'yearmonthday' format to file */
void addTime(std::string filename) {
	time_t now = time(0);
	tm *ltm = localtime(&now);
	string result = to_string(ltm->tm_year) + to_string(ltm->tm_mon) + to_string(ltm->tm_mday);
	ofstream outputFile(base + filename, fstream::app);
	outputFile << result << std::endl;
	uploadData();
}

/* Adds click to clickPlace.txt in format 'x \n y' */
void addPlaceClicked(int x, int y) {
	ofstream outputFile(base + "clickPlace.txt", fstream::app);
	outputFile << x << std::endl << y << std::endl;
}

/* All codes that have two keys will have exactly one key with a nonnull tiebreaker*/
std::string breakDuplicates(UINT code, char tiebreaker) {
	std::string alt = "";
	if (tiebreaker != NULL) {
		std::string out = "";
		out = out + tiebreaker;
		return out;
	} else {
		switch (code) {
			case 106: alt = "prtsc"; break;
			case 45: alt = "insert"; break;
			case 46: alt = "delete"; break;
			case 37: alt = "left"; break;
			case 38: alt = "up"; break;
			case 40: alt = "down"; break;
			case 39: alt = "right"; break;
			case 71: alt = "play"; break;
			case 81: alt = "rewind"; break;
			case 80: alt = "fastforward"; break;
			default: alt = "";
		}
		return alt;
	}

}

/* Add special characters */
std::string getSpecialTyped(UINT code, char tiebreaker) {
	std::string alt = "";
	switch (code) {
		case 192: alt = "`"; break;
		case 9: alt = "tab"; break;
		case 241: alt = "windows"; break;
		case 13: alt = "enter"; break;
		case 8: alt = "backspace"; break;
		case 68: alt = "mute"; break;
		case 112: alt = "f1"; break;
		case 113: alt = "f2"; break;
		case 114: alt = "f3"; break;
		case 115: alt = "f4"; break;
		case 116: alt = "f5"; break;
		case 117: alt = "f6"; break;
		case 118: alt = "f7"; break;
		case 119: alt = "f8"; break;
		case 120: alt = "f9"; break;
		case 121: alt = "f10"; break;
		case 122: alt = "f11"; break;
		case 123: alt = "f12"; break;
		case 189: alt = "-"; break;
		case 32: alt = " "; break;
		case 188: alt = ","; break;
		case 190: alt = "."; break;
		case 191: alt = "/"; break;
		case 109: alt = "-"; break;
		case 187: alt = "="; break;
		case 107: alt = "+"; break;
		case 36: alt = "7"; break;
		case 33: alt = "9"; break;
		case 12: alt = "5"; break;
		case 34: alt = "3"; break;
		case 71: alt = "play"; break;
		case 81: alt = "rewind"; break;
		case 80: alt = "fast forward"; break;
		case 20: alt = "caps"; break;
		case 16: alt = "shift"; break;
		case 17: alt = "ctrl"; break;
		case 144: alt = "num lock"; break;
		default: alt = breakDuplicates(code, tiebreaker);
	}
	return alt;
}

/* Adds keys to file */
void addCharTyped(UINT code, char tiebreaker) {
	std::string charTyped;
	if (((code >= 48 && code <= 57) || (code >= 65 && code <= 90)) && tiebreaker) {
		charTyped = char(code);
	} else {
		charTyped = getSpecialTyped(code, tiebreaker);
	}
	
	ofstream outputFile(base + "typeChar.txt", fstream::app);
	outputFile << charTyped << std::endl;
}

/* Called when key pressed, calls helpers to upload to txt files */
LRESULT __stdcall KeyHookCallback(int nCode, WPARAM wParam, LPARAM lParam) {
	if (nCode >= 0) {
		auto kbdStruct = *((KBDLLHOOKSTRUCT*)lParam);
		if (wParam == WM_KEYDOWN) {
			char c = MapVirtualKey(kbdStruct.vkCode, 2);
			UINT uCode = MapVirtualKey(kbdStruct.scanCode, 1);
			addCharTyped(uCode, c);
			addTime("typeTime.txt");
		}
	}
	return CallNextHookEx(mouseHook, nCode, wParam, lParam);
}

/* Called when mouse clicked, calls helpers to upload to txt files */
LRESULT __stdcall MouseHookCallback(int nCode, WPARAM wParam, LPARAM lParam) {
	if (nCode >= 0 && wParam == WM_LBUTTONDOWN) {
		POINT pt;
		GetCursorPos(&pt);
		addTime("clickTime.txt");
		addPlaceClicked(pt.x, pt.y);
	}
	return CallNextHookEx(mouseHook, nCode, wParam, lParam);
}

/* Sets hooks for mouse and keyboard */
void SetHook() {
	if (!(mouseHook = SetWindowsHookEx(WH_MOUSE_LL, MouseHookCallback, NULL, 0))) {
		cout << "Failed to install mouse hook!" << endl;
	}
	if (!(keyHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyHookCallback, NULL, 0))) {
		cout << "Failed to install keyboard hook!" << endl;
	}
}

/* Stops hooks from reacting */
void ReleaseHook() {
	UnhookWindowsHookEx(mouseHook);
	UnhookWindowsHookEx(keyHook);
}

//int main() {
//int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
/* Sets hooks and waits to react to mouse clicks and key presses */
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
	SetHook();
	MSG msg;

	while (GetMessage(&msg, NULL, 0, 0)) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
	return msg.wParam;
}