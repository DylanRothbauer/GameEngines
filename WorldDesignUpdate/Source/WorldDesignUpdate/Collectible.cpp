#include "Collectible.h"
#include "CharacterPlayerState.h"
#include "GameFramework/Character.h"

ACollectible::ACollectible()
{
}

void ACollectible::OnCollectibleOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& SweepResult)
{
    UE_LOG(LogTemp, Warning, TEXT("Collectible Overlapped"));
    if (OtherActor->ActorHasTag(FName("Player")))
    {
        UE_LOG(LogTemp, Warning, TEXT("Player Overlapped"));
        // Collectible Jar's model values should be added to the player's inventory
        ACharacter* Character = Cast<ACharacter>(OtherActor);
        if (Character)
        {
            ACharacterPlayerState* PlayerState = Cast<ACharacterPlayerState>(Character->GetPlayerState());
            if (PlayerState)
            {
                PlayerState->GetInventory()->AddItem(CollectibleValues);
                Destroy();
            }
        }
    }
}