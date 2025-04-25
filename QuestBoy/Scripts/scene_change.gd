extends Node

var next_world_path

# @onready var current_world = $"../Level 1"
@onready var anim = $CanvasLayer/AnimationPlayer

var is_fading = false

func _ready() -> void:
	print("AnimationPlayer found? ", anim != null)

func _on_animation_player_animation_finished(anim_name: StringName) -> void:
	if anim_name == "fade_in":
		var new_scene = load(next_world_path)
		if new_scene:
			get_tree().change_scene_to_packed(new_scene)
		else:
			push_error("Scene failed to load: " + str(next_world_path))
			
			
func play_fade_in():
	anim.play("fade_in")
func play_fade_out():
	anim.play("fade_out")
	
func transition_to_scene(path: String):
	print("Transitioning to: ", path)
	next_world_path = path
	anim.play("fade_in") # screen goes black
