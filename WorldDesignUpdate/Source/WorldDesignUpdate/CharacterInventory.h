#pragma once
#include "CollectibleValues.h"
#include "CharacterInventory.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnInventoryUpdated, int32, InventorySize);

UCLASS()
class WORLDDESIGNUPDATE_API UCharacterInventory : public UObject {
	GENERATED_BODY()

public:
	TArray<FCollectibleValues> Inventory;

	UFUNCTION(BlueprintCallable)
	TArray<FCollectibleValues> GetInventory();

	UFUNCTION(BlueprintCallable)
	void AddItem(FCollectibleValues Item);

	UFUNCTION(BlueprintCallable)
	FCollectibleValues GetItem();

	UFUNCTION(BlueprintCallable)
	int32 GetInventorySize();

	UFUNCTION(BlueprintCallable)
	void ClearInventory();

	// Funciton to add to the delegate
	UFUNCTION(BlueprintCallable)
	void AddToDelegate();

	UPROPERTY(BlueprintAssignable, BlueprintCallable)
	FOnInventoryUpdated OnInventoryUpdated;
};