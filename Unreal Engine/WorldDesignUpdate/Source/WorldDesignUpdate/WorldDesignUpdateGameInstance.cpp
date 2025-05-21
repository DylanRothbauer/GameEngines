#include "WorldDesignUpdateGameInstance.h"
#include "Runtime/Engine/Classes/Kismet/GamePlayStatics.h"


void UWorldDesignUpdateGameInstance::OnStart()
{
	UE_LOG(LogTemp, Warning, TEXT("GameInstance started - Initializing Lights and Enemies"))

    TArray<AActor*> TempLights;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ALightSource::StaticClass(), TempLights);

    for (AActor* Temp : TempLights)
    {
        ALightSource* Light = Cast<ALightSource>(Temp);
        if (Light)
        {
            Lights.Add(Light);
            Light->OnLightSourceUpdated.AddDynamic(this, &UWorldDesignUpdateGameInstance::CheckAllLights);
            UE_LOG(LogTemp, Warning, TEXT("Delegate bound for Light: %s"), *Light->GetName())
        }
    }

    TArray<AActor*> TempEnemies;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), AEnemy::StaticClass(), TempEnemies);

    for (AActor* Temp : TempEnemies)
    {
        AEnemy* Enemy = Cast<AEnemy>(Temp);
        if (Enemy)
        {
            Enemies.Add(Enemy);
        }
    }

    Player = Cast<AWorldDesignUpdateCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));

    UE_LOG(LogTemp, Warning, TEXT("Finished initializing %d lights and %d enemies."), Lights.Num(), Enemies.Num());
}

void UWorldDesignUpdateGameInstance::SetAllLights(bool turnOn)
{
    UE_LOG(LogTemp, Warning, TEXT("SetAllLights()!"))

    for (ALightSource* Light : Lights)
    {
        if (Light)
        {
            Light->SetLightState(turnOn);
        }
    }
}

bool UWorldDesignUpdateGameInstance::AreAllLightsOn()
{
    UE_LOG(LogTemp, Warning, TEXT("AreAllLightsOn()!"))

    for (ALightSource* Light : Lights)
    {
        if (!Light || !Light->LightOn)
        {
            return false;
        }
    }
    return true;
}

void UWorldDesignUpdateGameInstance::RemoveAllEnemies()
{
    UE_LOG(LogTemp, Warning, TEXT("RemoveAllEnemies()!"))
    for (AEnemy* Enemy : Enemies)
    {
        if (Enemy)
        {
            Enemy->Destroy();
        }
    }

    // Clear the enemy list
    Enemies.Empty();
}

void UWorldDesignUpdateGameInstance::CheckAllLights(bool LightOn)
{
    UE_LOG(LogTemp, Warning, TEXT("CheckAllLights called! LightOn: %d"), LightOn)

    if (AreAllLightsOn())
    {
        UE_LOG(LogTemp, Warning, TEXT("All lights are on! Removing enemies..."))

        RemoveAllEnemies();
    }
}
