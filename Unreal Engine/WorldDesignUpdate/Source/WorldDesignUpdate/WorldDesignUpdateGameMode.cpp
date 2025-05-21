// Copyright Epic Games, Inc. All Rights Reserved.

#include "WorldDesignUpdateGameMode.h"
#include "WorldDesignUpdateCharacter.h"
#include "UObject/ConstructorHelpers.h"
#include "CharacterPlayerState.h"
#include "CharacterInventory.h"

AWorldDesignUpdateGameMode::AWorldDesignUpdateGameMode()
	: Super()
{
	// set default pawn class to our Blueprinted character
	static ConstructorHelpers::FClassFinder<APawn> PlayerPawnClassFinder(TEXT("/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter"));
	DefaultPawnClass = PlayerPawnClassFinder.Class;


	// Lookup & Update PlayerStateClass
	static ConstructorHelpers::FClassFinder<ACharacterPlayerState> CharacterPlayerState(TEXT("/Script/WorldDesignUpdate.CharacterPlayerState"));

	if (CharacterPlayerState.Class != NULL)
	{
		PlayerStateClass = CharacterPlayerState.Class;
	}
}
