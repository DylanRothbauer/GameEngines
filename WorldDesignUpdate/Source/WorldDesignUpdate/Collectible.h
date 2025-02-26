#pragma once
#include "CollectibleValues.h"
#include <Components/BoxComponent.h>
#include "Collectible.generated.h"

UCLASS()
class WORLDDESIGNUPDATE_API ACollectible : public AActor {
	GENERATED_BODY()
public:
	ACollectible();

protected:

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FCollectibleValues CollectibleValues;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	UBoxComponent* CollectibleCollider;

	UFUNCTION()
	void OnCollectibleOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& SweepResult);
};