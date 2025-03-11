#pragma once
#include <Components/BoxComponent.h>
#include <Components/SpotLightComponent.h>
#include "LightSource.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLightSourceUpdated, bool, LightOn);

UCLASS()
class WORLDDESIGNUPDATE_API ALightSource : public AActor {
	GENERATED_BODY()
public:
	ALightSource();

protected:

	virtual void BeginPlay() override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	UBoxComponent* LightSourceCollider;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	USpotLightComponent* SpotLight;

	UFUNCTION()
	void OnLightSourceOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool FromSweep, const FHitResult& SweepResult);

	UFUNCTION()
	void ToggleLight();

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FOnLightSourceUpdated OnLightSourceUpdated;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	bool LightOn;
};