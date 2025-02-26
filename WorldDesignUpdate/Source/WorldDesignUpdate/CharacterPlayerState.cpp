#include "CharacterPlayerState.h"

ACharacterPlayerState::ACharacterPlayerState()
{
	Inventory = NewObject<UCharacterInventory>(this);
}

UCharacterInventory* ACharacterPlayerState::GetInventory()
{
    if (Inventory)
    {
        return Inventory;
    }
	return nullptr;

}
