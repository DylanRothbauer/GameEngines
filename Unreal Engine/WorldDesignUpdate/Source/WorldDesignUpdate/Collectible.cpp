#include "Collectible.h"
#include "CharacterPlayerState.h"
#include "GameFramework/Character.h"

ACollectible::ACollectible()
{
    UE_LOG(LogTemp, Warning, TEXT("Jar constructed"))

    CollectibleCollider = this->CreateDefaultSubobject<UBoxComponent>(TEXT("CollectibleCollider"));
    CollectibleCollider->SetupAttachment(RootComponent);
    //RootComponent = Cast<UBoxComponent>(CollectibleCollider);
    CollectibleCollider->SetRelativeScale3D(FVector(4.0, 4.0, 2.0));
}

void ACollectible::BeginPlay() {
    //CollectibleCollider->OnComponentBeginOverlap.AddDynamic(this, &ACollectible::OnCollectibleOverlap);

    UE_LOG(LogTemp, Warning, TEXT("Jar BeginPlay"))
    CollectibleCollider->OnComponentBeginOverlap.AddDynamic(this, &ACollectible::OnCollectibleOverlap);
}

void ACollectible::OnCollectibleOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool FromSweep, const FHitResult& SweepResult)
{
    UE_LOG(LogTemp, Warning, TEXT("Collectible Overlapped"));
    if (OtherActor->ActorHasTag(FName("Player")))
    {
        UE_LOG(LogTemp, Warning, TEXT("Player Overlapped"));
        // Collectible Jar's model values should be added to the player's inventory
        ACharacter* Character = Cast<ACharacter>(OtherActor);
        if (Character)
        {
            UE_LOG(LogTemp, Warning, TEXT("CHARACTER IS GOOD"));
            ACharacterPlayerState* PlayerState = Cast<ACharacterPlayerState>(Character->GetPlayerState());
            if (PlayerState)
            {
                PlayerState->GetInventory()->AddItem(CollectibleValues);
                UE_LOG(LogTemp, Warning, TEXT("PLAYER STATE IS GOOD - ADDED ITEM"));
                CollectibleCollider->DestroyComponent();
                Destroy();
				
                
            }
        }
    }
}