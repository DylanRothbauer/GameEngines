extends Node

var player : Node = null
var level_states = {}  # Stores data for each level
var player_health = 5
var player_max_health = 5


signal health_changed(value)


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func notify_health_change(new_health):
	emit_signal("health_changed", new_health)


func save_level_state(level_name: String, data: Dictionary):
	level_states[level_name] = data

func get_level_state(level_name: String) -> Dictionary:
	return level_states.get(level_name, {})
