#pragma once
#include "CollectibleValues.generated.h"

USTRUCT(Blueprintable)
struct WORLDDESIGNUPDATE_API FCollectibleValues
{
	GENERATED_BODY()

public:

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FName Type;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 Value;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 Id;
};