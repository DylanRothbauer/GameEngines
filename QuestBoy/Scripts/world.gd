extends Node2D

signal world_changed(world_name)

var entered = false
var recently_loaded = true
var defeated_enemies = []
var doors = []

@export var world_name : String = "world"
@onready var player = $Player
@onready var enemies = []


func _ready() -> void:
	enemies = $Enemies.get_children()

	# Connect signals
	for enemy in enemies:
		if enemy.has_signal("slime_defeated"):
			enemy.connect("slime_defeated", _on_enemy_defeated)
		
	# Connect door signals
	for door in get_tree().get_nodes_in_group("Door"):
		door.connect("onHit", _on_door_used)
	
	load_state()
	print("SHOULD PLAY FADE OUT")
	SceneChange.play_fade_out()

func _process(delta: float) -> void:
	if recently_loaded:
		await get_tree().create_timer(0.2).timeout
		recently_loaded = false
		entered = false
		
func _on_enemy_defeated(enemy_name: String):
	print("Defeated enemy:", enemy_name)
	if not defeated_enemies.has(enemy_name):
		defeated_enemies.append(enemy_name)

func _on_door_used(target_scene: String) -> void:
	print("Door used, target_scene:", target_scene)
	if not entered and not recently_loaded:
		entered = true
		save_state()
		SceneChange.transition_to_scene("res://Scenes/" + target_scene + ".tscn")
				
				
func _on_area_2d_body_exited(body: Node):
	entered = false

# Save player position and defeated enemies
func save_state():
	GameState.save_level_state(world_name, {
		"player_pos": player.global_position,
		"defeated_enemies": defeated_enemies
	})

# Load previously saved state if it exists
func load_state():
	var state = GameState.get_level_state(world_name)
	if state:
		if state.has("player_pos"):
			player.global_position = state["player_pos"]
		if state.has("defeated_enemies"):
			defeated_enemies = state["defeated_enemies"]
			for enemy in enemies:
				if enemy.name in defeated_enemies:
					enemy.queue_free()
