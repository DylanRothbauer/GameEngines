#pragma once
#include "CollectibleValues.h"
#include "Engine/StaticMeshActor.h"
#include <Components/BoxComponent.h>
#include "Collectible.generated.h"

UCLASS()
class WORLDDESIGNUPDATE_API ACollectible : public AStaticMeshActor {
	GENERATED_BODY()
public:
	ACollectible();

protected:

	virtual void BeginPlay() override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FCollectibleValues CollectibleValues;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	UBoxComponent* CollectibleCollider;

	UFUNCTION()
	void OnCollectibleOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool FromSweep, const FHitResult& SweepResult);
};