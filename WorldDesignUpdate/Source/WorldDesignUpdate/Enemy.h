#pragma once
#include "WorldDesignUpdateCharacter.h"
#include "Enemy.generated.h"

UCLASS()
class WORLDDESIGNUPDATE_API AEnemy : public APawn {
	GENERATED_BODY()
public:
	AEnemy();

protected:

	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	bool WasPlayerSeen;
	FVector StartLocation;

	bool GetPlayerSeen() { return WasPlayerSeen; }
	FVector GetStartLocation() { return StartLocation; }

	UFUNCTION()
	void LookForPlayer();

	UFUNCTION()
	void MoveToPlayer(float DeltaTime);

	UFUNCTION()
	void MoveToLocation(FVector Location, float DeltaTime);

	UFUNCTION()
	void RotateToPlayer(float DeltaTime);

	UFUNCTION()
	bool IsPlayerFacingAway();

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	float MoveSpeed = 300.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	float FieldOfView = 30.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	float ViewLength = 1000.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	float StopDistance = 200.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	float RotateSpeed = 90.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FVector LastPlayerPosition;


};