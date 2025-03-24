#include "LightSource.h"
#include "GameFramework/Character.h"
#include "LampStates.h"


ALightSource::ALightSource()
{
    UE_LOG(LogTemp, Warning, TEXT("LightSource constructed"))
    LightOn = false;
    LightSourceCollider = this->CreateDefaultSubobject<UBoxComponent>(TEXT("LightSourceCollider"));
    LightSourceCollider->SetupAttachment(RootComponent);
    LightSourceCollider->SetRelativeScale3D(FVector(4.0, 4.0, 2.0));

    SpotLight = this->CreateDefaultSubobject<USpotLightComponent>(TEXT("SpotLight"));
    SpotLight->SetupAttachment(LightSourceCollider);
    SpotLight->SetRelativeLocation(FVector(0.0f, 0.0f, 100.0f));
    SpotLight->SetIntensity(50000.0f);
    SpotLight->SetVisibility(LightOn);

    // State Machine Stuff
    CurrentState = OffLampState::GetInstance();
    StateMachineValues.GameInstance = (UWorldDesignUpdateGameInstance*)GetGameInstance();
    StateMachineValues.isPlayerNear = false;
    StateMachineValues.TimeinState = 0.0f;
}

void ALightSource::BeginPlay()
{
    UE_LOG(LogTemp, Warning, TEXT("LightSource BeginPlay"))
    LightSourceCollider->OnComponentBeginOverlap.AddDynamic(this, &ALightSource::OnLightSourceOverlap);
}

void ALightSource::OnLightSourceOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool FromSweep, const FHitResult& SweepResult)
{
    // OnLightSourceUpdated.Broadcast
    UE_LOG(LogTemp, Warning, TEXT("LightSource Overlapped"));
    if (OtherActor->ActorHasTag(FName("Player")))
    {
        ACharacter* Character = Cast<ACharacter>(OtherActor);
        if (Character)
        {
            UE_LOG(LogTemp, Warning, TEXT("CHARACTER GOOD -> TOGGLELIGHT()"));
            ToggleLight();
        }
    }

}

void ALightSource::ToggleLight()
{
    UE_LOG(LogTemp, Warning, TEXT("ToggleLight() - Entering Function"));

    LightOn = !LightOn;
    //USpotLightComponent* SpotLight = FindComponentByClass<USpotLightComponent>();
    //ULightComponent* LightComponent = FindComponentByClass<ULightComponent>();

    if (SpotLight)
    {
        SpotLight->SetVisibility(LightOn);
        SpotLight->SetIntensity(LightOn ? 5000.0f : 0.0f);
        UE_LOG(LogTemp, Warning, TEXT("SpotLight toggled: %s"), LightOn ? TEXT("On") : TEXT("Off"));
    }
    else
    {
        UE_LOG(LogTemp, Warning, TEXT("SpotLight NOT found!"));
    }

    OnLightSourceUpdated.Broadcast(LightOn);
    UE_LOG(LogTemp, Warning, TEXT("Light state changed: %s"), LightOn ? TEXT("On") : TEXT("Off"));
}

void ALightSource::SetLightState(bool turnOn)
{
    LightOn = turnOn;

    if (SpotLight)
    {
        SpotLight->SetVisibility(LightOn);
        SpotLight->SetIntensity(LightOn ? 5000.0f : 0.0f);
    }

    OnLightSourceUpdated.Broadcast(LightOn);
}
