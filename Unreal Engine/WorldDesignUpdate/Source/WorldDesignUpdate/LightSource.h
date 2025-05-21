#pragma once
#include <Components/BoxComponent.h>
#include <Components/SpotLightComponent.h>
#include "LampStateMachine.h"
#include "LightSource.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLightSourceUpdated, bool, LightOn);

// forward declaration
class LampState;

UCLASS()
class WORLDDESIGNUPDATE_API ALightSource : public AActor {
	GENERATED_BODY()
public:
	ALightSource();

	UPROPERTY(BlueprintAssignable, BlueprintCallable)
	FOnLightSourceUpdated OnLightSourceUpdated;

	void SetLightState(bool turnOn);

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	bool LightOn;

	virtual void Tick(float DeltaTime) override;
	FTimerHandle SimulatedTickHandle;
	void SimulatedTick();

protected:

	virtual void BeginPlay() override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	UBoxComponent* LightSourceCollider;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	USpotLightComponent* SpotLight;

	UFUNCTION()
	void OnLightSourceOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool FromSweep, const FHitResult& SweepResult);

	UFUNCTION()
	void OnWarningOverlapEnd(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);

	UFUNCTION()
	void ToggleLight();

	// State Machine variables
	/*LampState* CurrentState;
	float TimeinState;
	bool isPlayerNear;*/
	LampState* CurrentState;
	LampStateMachine StateMachineValues;
	
};