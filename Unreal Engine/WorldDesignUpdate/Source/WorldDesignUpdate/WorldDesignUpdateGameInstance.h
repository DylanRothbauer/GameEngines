#pragma once
#include "CoreMinimal.h"
#include "Engine/GameInstance.h"
#include "LightSource.h"
#include "Enemy.h"
#include "WorldDesignUpdateCharacter.h"
#include "WorldDesignUpdateGameInstance.generated.h"


UCLASS()
class WORLDDESIGNUPDATE_API UWorldDesignUpdateGameInstance : public UGameInstance
{
	GENERATED_BODY()

public:
    //static UWorldDesignGameInstance* Get(UWorld* World);

    // Note: Make these private in the future
    UPROPERTY()
    TArray<ALightSource*> Lights;

    UPROPERTY()
    TArray<AEnemy*> Enemies;

    UPROPERTY()
    AWorldDesignUpdateCharacter* Player;

    // Functions
    void SetAllLights(bool turnOn);
    bool AreAllLightsOn();
    void RemoveAllEnemies();

    void OnStart();

    UFUNCTION()
    void CheckAllLights(bool LightOn);
};