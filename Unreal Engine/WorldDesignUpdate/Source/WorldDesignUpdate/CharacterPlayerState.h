#pragma once
#include "GameFramework/PlayerState.h"
#include "CharacterInventory.h"
#include "CharacterPlayerState.generated.h"

UCLASS()
class WORLDDESIGNUPDATE_API ACharacterPlayerState : public APlayerState {
	GENERATED_BODY()

public:
	ACharacterPlayerState();

	UFUNCTION(BlueprintCallable)
	UCharacterInventory* GetInventory();

	// Pointer to inventory class
	UPROPERTY()
	UCharacterInventory* Inventory;

};