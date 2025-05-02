extends HBoxContainer

var heart_full = preload("res://Assets/heart_full.png.tres")
var heart_empty = preload("res://Assets/heart_empty.png.tres")

# Called when the node enters the scene tree for the first time.
func _ready():
	#GameState.connect("health_changed", Callable(self, "update_health"))
	call_deferred("_wait_for_player")
		
	#GameState.player.connect("health_changed", Callable(self, "update_health"))
	check_scene_visibility()

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
	
func _wait_for_player():
	await get_tree().process_frame  # Wait 1 frame to ensure Player is in tree
	while GameState.player == null:
		await get_tree().process_frame
	print("Player found for health")
	GameState.player.connect("health_changed", Callable(self, "update_health"))
	update_health(GameState.player_health)  # Sync HUD immediately

func _connect_to_player():
	if GameState.player:
		print("Player found for health")
		GameState.player.connect("health_changed", Callable(self, "update_health"))
	else:
		print("Player NOT found for health")

func update_health(value: int):
	print("Updating HUD Health:", value)
	for i in range(get_child_count()):
		var heart = get_child(i)
		if value > i:
			heart.texture = heart_full
		else:
			heart.texture = heart_empty
			

func check_scene_visibility():
	var current_scene_name = get_tree().current_scene.name
	if current_scene_name == "MainMenu":
		hide()
	else:
		show()

func _on_scene_changed():
	check_scene_visibility()
