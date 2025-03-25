#include "LampStates.h"
#include "WorldDesignUpdateGameInstance.h"

void OffLampState::Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	UE_LOG(LogTemp, Warning, TEXT("OFFLAMPSTATE EXECUTE"));
	Lamp->SetLightState(false);
}

LampState* OffLampState::GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	UE_LOG(LogTemp, Warning, TEXT("OFFLAMPSTATE GETNEXTSTATE"));
	if (StateMachine.isPlayerNear) {
		return OnNearLampState::GetInstance();
	}
	return this;
}

OffLampState* OffLampState::GetInstance()
{
	UE_LOG(LogTemp, Warning, TEXT("OFFLAMPSTATE GETINSTANCE"));
	static OffLampState Instance;
	return &Instance;
}

void OnNearLampState::Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	UE_LOG(LogTemp, Warning, TEXT("ONNEARLAMPSTATE EXECUTE"));
	Lamp->SetLightState(true);
}

LampState* OnNearLampState::GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	UE_LOG(LogTemp, Warning, TEXT("ONNEARLAMPSTATE GETNEXTSTATE %p"), StateMachine.GameInstance);
	// Check if all are on!
	if (StateMachine.GameInstance->AreAllLightsOn()) {
		return AlwaysOnLampState::GetInstance();
	}

	if (!StateMachine.isPlayerNear) {
		return OnLampState::GetInstance();
	}
	return this;
}

OnNearLampState* OnNearLampState::GetInstance()
{
	UE_LOG(LogTemp, Warning, TEXT("ONNEARLAMPSTATE GETINSTANCE"));
	static OnNearLampState Instance;
	return &Instance;
}

void OnLampState::Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	UE_LOG(LogTemp, Warning, TEXT("ONLAMPSTATE EXECUTE"));
	// Not sure (maybe keep track of time)
}

LampState* OnLampState::GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	UE_LOG(LogTemp, Warning, TEXT("ONLAMPSTATE GETNEXTSTATE"));

	// Check if all are on!
	if (StateMachine.GameInstance->AreAllLightsOn()) {
		return AlwaysOnLampState::GetInstance();
	}

	if (StateMachine.isPlayerNear) {
		return OnNearLampState::GetInstance();
	}

	if (StateMachine.TimeinState >= 5.0f) {
		Lamp->SetLightState(false); // clean up later
		return OffLampState::GetInstance();
	}

	return this;
}

OnLampState* OnLampState::GetInstance()
{
	UE_LOG(LogTemp, Warning, TEXT("ONLAMPSTATE GETINSTANCE"));

	static OnLampState Instance;
	return &Instance;
}

void AlwaysOnLampState::Execute(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	UE_LOG(LogTemp, Warning, TEXT("ALWAYSONLAMPSTATE EXECUTE"));

	Lamp->SetLightState(true);
}

LampState* AlwaysOnLampState::GetNextState(ALightSource* Lamp, float DeltaTime, LampStateMachine StateMachine)
{
	UE_LOG(LogTemp, Warning, TEXT("ALWAYSONLAMPSTATE GETNEXTSTATE"));

	if (StateMachine.GameInstance->AreAllLightsOn()) {
		return this;
	}

	return OffLampState::GetInstance();
}

AlwaysOnLampState* AlwaysOnLampState::GetInstance()
{
	UE_LOG(LogTemp, Warning, TEXT("ALWAYSONLAMPSTATE GETINSTANCE"));

	static AlwaysOnLampState Instance;
	return &Instance;
}
