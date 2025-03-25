#include "Enemy.h"
#include "Components/ArrowComponent.h"
#include "Runtime/Engine/Classes/Kismet/GamePlayStatics.h"

AEnemy::AEnemy()
{
	PrimaryActorTick.bCanEverTick = true;
	UE_LOG(LogTemp, Warning, TEXT("Enemy constructed"))

}

void AEnemy::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogTemp, Warning, TEXT("Enemy BeginPlay"))
	FTimerHandle LookHandle;
	GetWorld()->GetTimerManager().SetTimer(LookHandle, this,
		&AEnemy::LookForPlayer, 0.1f, true);

	GetWorld()->GetTimerManager().SetTimer(SimulatedTickHandle, this,
		&AEnemy::SimulatedTick, 0.05f, true);

	StartLocation = GetActorLocation();
}

void AEnemy::SimulatedTick()
{
	float DeltaTime = 0.05f;

	//UE_LOG(LogTemp, Warning, TEXT("Simulated Tick!"))

		if (WasPlayerSeen)
		{
			RotateToPlayer(DeltaTime);

			if (IsPlayerFacingAway())
			{
				MoveToPlayer(DeltaTime);
			}
		}
}

void AEnemy::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

	//UE_LOG(LogTemp, Warning, TEXT("Enemy Tick!"))

    if (WasPlayerSeen && IsPlayerFacingAway())
    {
        RotateToPlayer(DeltaTime);
        MoveToPlayer(DeltaTime);
    }
}

void AEnemy::LookForPlayer()
{
	FVector StartPos = this->GetActorLocation() + FVector(0.0f, 0.0f, 100.0f);
	FVector ToPlayer;

	AWorldDesignUpdateCharacter* Player = Cast<AWorldDesignUpdateCharacter>(
		UGameplayStatics::GetPlayerCharacter(GetWorld(), 0)
	);

	if (Player)
	{
		//UE_LOG(LogTemp, Warning, TEXT("Player Found"))
		ToPlayer = Player->GetActorLocation() - StartPos;
		ToPlayer.Normalize();
	}

	FVector EndPos = StartPos + ToPlayer * ViewLength;

	FName RobotSight("RobotSight");
	FCollisionQueryParams QueryParams(RobotSight, false, this);
	FHitResult Hit;

	GetWorld()->DebugDrawTraceTag = RobotSight;

	bool WasHit = GetWorld()->LineTraceSingleByChannel(Hit, StartPos, EndPos, ECC_PhysicsBody, QueryParams);

	WasPlayerSeen = false;
	if (WasHit && Hit.GetActor() && Hit.GetActor()->ActorHasTag(FName("Player")))
	{
		//UE_LOG(LogTemp, Warning, TEXT("Enemy saw the player!"))
		FVector Forward = GetComponentByClass<UArrowComponent>()->GetForwardVector();
		Forward.Normalize();

		float Dot = Forward.Dot(ToPlayer);
		float Angle = FMath::RadiansToDegrees(FMath::Acos(Dot));

		/*UE_LOG(LogTemp, Warning, TEXT("Angle: %f"), Angle);
		UE_LOG(LogTemp, Warning, TEXT("Field of View: %f"), FieldOfView);*/

		if (Angle <= FieldOfView)
		{
			LastPlayerPosition = Hit.GetActor()->GetActorLocation();
			WasPlayerSeen = true;
		}
	}
}

void AEnemy::MoveToPlayer(float DeltaTime)
{
	MoveToLocation(LastPlayerPosition, DeltaTime);
}

void AEnemy::MoveToLocation(FVector Location, float DeltaTime)
{
	//UE_LOG(LogTemp, Warning, TEXT("MoveToLocation()!"))
	FVector ToLocation = Location - GetActorLocation();
	float DistanceToLocation = ToLocation.Length();
	ToLocation.Z = 0;
	ToLocation.Normalize();

	if (DistanceToLocation <= StopDistance) {
		UE_LOG(LogTemp, Warning, TEXT("Enemy stopped at StopDistance: %f"), StopDistance)
		return;
	}

	float Distance = DeltaTime * MoveSpeed;

	if (DistanceToLocation < Distance)
	{
		SetActorLocation(GetStartLocation(), true);
		UE_LOG(LogTemp, Warning, TEXT("Enemy reached target"))
	}
	else
	{
		FVector NewLocation = GetActorLocation() + ToLocation * Distance;
		SetActorLocation(NewLocation, true);
	}
}

void AEnemy::RotateToPlayer(float DeltaTime)
{
	//UE_LOG(LogTemp, Warning, TEXT("RotateToPlayer()!"))
	FVector ToPlayer = LastPlayerPosition - GetActorLocation();
	ToPlayer.Z = 0;
	ToPlayer.Normalize();

	FVector Forward = GetComponentByClass<UArrowComponent>()->GetForwardVector();
	Forward.Normalize();

	float Dot = Forward.Dot(ToPlayer);
	float Angle = FMath::RadiansToDegrees(FMath::Acos(Dot));

	float AngleToTurn = FMath::Clamp(RotateSpeed * DeltaTime, 0.0f, Angle);

	FVector Cross = Forward.Cross(ToPlayer);
	if (Cross.Z < 0)
	{
		AngleToTurn *= -1;
	}

	FRotator NewRotation = GetActorRotation();
	NewRotation.Yaw += AngleToTurn;
	SetActorRotation(NewRotation);
}

bool AEnemy::IsPlayerFacingAway()
{
	//UE_LOG(LogTemp, Warning, TEXT("IsPlayerFacingAway()!"))
	AWorldDesignUpdateCharacter* Player = Cast<AWorldDesignUpdateCharacter>(
		UGameplayStatics::GetPlayerCharacter(GetWorld(), 0)
	);

	if (!Player) return false;

	FVector ToEnemy = GetActorLocation() - Player->GetActorLocation();
	ToEnemy.Normalize();

	FVector PlayerForward = Player->GetActorForwardVector();
	PlayerForward.Normalize();

	// If negative, player is facing away
	return (PlayerForward.Dot(ToEnemy) < 0);
}
