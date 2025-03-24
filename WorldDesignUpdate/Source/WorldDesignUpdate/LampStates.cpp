#include "LampStates.h"
#include "WorldDesignUpdateGameInstance.h"

void OffLampState::Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	Lamp->SetLightState(false);
}

LampState* OffLampState::GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	if (StateMachine.isPlayerNear) {
		return OnNearLampState::GetInstance();
	}
	return this;
}

OffLampState* OffLampState::GetInstance()
{
	static OffLampState Instance;
	return &Instance;
}

void OnNearLampState::Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	Lamp->SetLightState(true);
}

LampState* OnNearLampState::GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	if (!StateMachine.isPlayerNear) {
		return OnLampState::GetInstance();
	}
	return this;
}

OnNearLampState* OnNearLampState::GetInstance()
{
	static OnNearLampState Instance;
	return &Instance;
}

void OnLampState::Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	// Not sure (maybe keep track of time)
}

LampState* OnLampState::GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	if (StateMachine.isPlayerNear) {
		return OnNearLampState::GetInstance();
	}

	if (StateMachine.TimeinState >= 5.0f) {
		Lamp->SetLightState(false);
		return OffLampState::GetInstance();
	}

	return this;
}

OnLampState* OnLampState::GetInstance()
{
	static OnLampState Instance;
	return &Instance;
}

void AlwaysOnLampState::Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	Lamp->SetLightState(true);
}

LampState* AlwaysOnLampState::GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	if (StateMachine.GameInstance->AreAllLightsOn()) {
		return this;
	}

	return OffLampState::GetInstance();
}

AlwaysOnLampState* AlwaysOnLampState::GetInstance()
{
	static AlwaysOnLampState Instance;
	return &Instance;
}
