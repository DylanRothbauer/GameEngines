#include "CharacterInventory.h"

UCharacterInventory::UCharacterInventory()
{
}

void UCharacterInventory::AddItem(FCollectibleValues Item)
{
	Inventory.Add(Item);
	OnInventoryUpdated.Broadcast(Inventory.Num());
}

FCollectibleValues UCharacterInventory::GetItem()
{
	return FCollectibleValues();
}

int32 UCharacterInventory::GetInventorySize()
{
	return Inventory.Num();
}

void UCharacterInventory::ClearInventory()
{
	Inventory.Empty();
	OnInventoryUpdated.Broadcast(Inventory.Num());
}

// Funciton to add to the delegate
void UCharacterInventory::AddToDelegate()
{
	UE_LOG(LogTemp, Warning, TEXT("Inventory Updated - Number of collectibles collected [{num}], num"));
	OnInventoryUpdated.Broadcast(Inventory.Num());
}

TArray<FCollectibleValues> UCharacterInventory::GetInventory()
{
	return Inventory;
}
