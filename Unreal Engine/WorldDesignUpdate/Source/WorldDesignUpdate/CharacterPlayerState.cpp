#include "CharacterPlayerState.h"

ACharacterPlayerState::ACharacterPlayerState()
{
    UE_LOG(LogTemp, Warning, TEXT("ACharacterPlayerState Constructor Called"));
    FName MyName = "MyName";

    //Inventory = CreateDefaultSubobject<UCharacterInventory>(TEXT("MYNAME"));
    Inventory = NewObject<UCharacterInventory>();

    if (Inventory)
    {
        UE_LOG(LogTemp, Warning, TEXT("Inventory successfully created"));
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to create Inventory"));
    }
}

UCharacterInventory* ACharacterPlayerState::GetInventory()
{
    if (Inventory)
    {
        return Inventory;
    }
    return nullptr;

}
