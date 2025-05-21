#pragma once

class UWorldDesignUpdateGameInstance;

class WORLDDESIGNUPDATE_API LampStateMachine {

public:
	// State Machine variables
	float TimeinState;
	bool isPlayerNear;
	UWorldDesignUpdateGameInstance* GameInstance;
};