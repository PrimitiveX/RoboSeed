# pre-train → post-train diagnostics: RoboTwin per-task Clean counts

[Diagnostic summary](pre-train-to-post-train-diagnostic.md)

Source: `exp.zip/exp/实验记录1.txt`; 50 tasks, 10 episodes each, seed 0. The local Qwen3-VL 4B pre-train→post-train model was not evaluated. The local 8B evaluator had GPU scheduling errors with later task reruns; interpret that column with care.

| Task | 2B local pre-train h16 | 2B local pre-train h50 | 8B local pre-train | published post-train | published pre-train→local post-train dim1024 | published pre-train→local post-train dim2560 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| adjust_bottle | 6/10 | 4/10 | 7/10 | 10/10 | 10/10 | 10/10 |
| beat_block_hammer | 4/10 | 0/10 | 1/10 | 9/10 | 7/10 | 10/10 |
| blocks_ranking_rgb | 0/10 | 0/10 | 0/10 | 8/10 | 9/10 | 8/10 |
| blocks_ranking_size | 0/10 | 1/10 | 0/10 | 7/10 | 2/10 | 4/10 |
| click_alarmclock | 2/10 | 0/10 | 0/10 | 7/10 | 0/10 | 0/10 |
| click_bell | 5/10 | 3/10 | 0/10 | 9/10 | 1/10 | 4/10 |
| dump_bin_bigbin | 1/10 | 3/10 | 5/10 | 10/10 | 9/10 | 10/10 |
| grab_roller | 4/10 | 3/10 | 4/10 | 10/10 | 10/10 | 10/10 |
| handover_block | 0/10 | 1/10 | 0/10 | 5/10 | 5/10 | 6/10 |
| handover_mic | 4/10 | 2/10 | 8/10 | 10/10 | 10/10 | 10/10 |
| hanging_mug | 0/10 | 0/10 | 0/10 | 2/10 | 3/10 | 0/10 |
| lift_pot | 0/10 | 1/10 | 4/10 | 10/10 | 9/10 | 10/10 |
| move_can_pot | 0/10 | 0/10 | 4/10 | 8/10 | 8/10 | 6/10 |
| move_pillbottle_pad | 0/10 | 0/10 | 0/10 | 8/10 | 8/10 | 9/10 |
| move_playingcard_away | 1/10 | 1/10 | 0/10 | 10/10 | 10/10 | 9/10 |
| move_stapler_pad | 0/10 | 0/10 | 0/10 | 6/10 | 1/10 | 5/10 |
| open_laptop | 4/10 | 4/10 | 4/10 | 10/10 | 10/10 | 9/10 |
| open_microwave | 3/10 | 5/10 | 3/10 | 8/10 | 8/10 | 10/10 |
| pick_diverse_bottles | 0/10 | 0/10 | 0/10 | 9/10 | 7/10 | 7/10 |
| pick_dual_bottles | 0/10 | 0/10 | 0/10 | 7/10 | 4/10 | 6/10 |
| place_a2b_left | 0/10 | 0/10 | 0/10 | 9/10 | 9/10 | 9/10 |
| place_a2b_right | 0/10 | 0/10 | 0/10 | 9/10 | 5/10 | 6/10 |
| place_bread_basket | 2/10 | 1/10 | 0/10 | 10/10 | 10/10 | 10/10 |
| place_bread_skillet | 0/10 | 0/10 | 0/10 | 8/10 | 9/10 | 10/10 |
| place_burger_fries | 0/10 | 3/10 | 2/10 | 10/10 | 8/10 | 9/10 |
| place_can_basket | 0/10 | 0/10 | 1/10 | 8/10 | 6/10 | 8/10 |
| place_cans_plasticbox | 1/10 | 1/10 | 0/10 | 10/10 | 10/10 | 10/10 |
| place_container_plate | 4/10 | 4/10 | 7/10 | 10/10 | 9/10 | 10/10 |
| place_dual_shoes | 0/10 | 0/10 | 0/10 | 7/10 | 7/10 | 5/10 |
| place_empty_cup | 1/10 | 0/10 | 0/10 | 10/10 | 10/10 | 10/10 |
| place_fan | 0/10 | 0/10 | 0/10 | 9/10 | 9/10 | 10/10 |
| place_mouse_pad | 0/10 | 0/10 | 0/10 | 6/10 | 5/10 | 3/10 |
| place_object_basket | 0/10 | 3/10 | 2/10 | 9/10 | 9/10 | 9/10 |
| place_object_scale | 0/10 | 0/10 | 0/10 | 8/10 | 8/10 | 9/10 |
| place_object_stand | 0/10 | 0/10 | 3/10 | 10/10 | 9/10 | 10/10 |
| place_phone_stand | 0/10 | 0/10 | 0/10 | 9/10 | 9/10 | 5/10 |
| place_shoe | 1/10 | 1/10 | 1/10 | 10/10 | 9/10 | 9/10 |
| press_stapler | 5/10 | 8/10 | 3/10 | 9/10 | 9/10 | 8/10 |
| put_bottles_dustbin | 0/10 | 1/10 | 0/10 | 7/10 | 4/10 | 5/10 |
| put_object_cabinet | 0/10 | 2/10 | 1/10 | 9/10 | 9/10 | 9/10 |
| rotate_qrcode | 0/10 | 1/10 | 0/10 | 8/10 | 8/10 | 8/10 |
| scan_object | 0/10 | 0/10 | 0/10 | 9/10 | 9/10 | 9/10 |
| shake_bottle | 4/10 | 4/10 | 3/10 | 10/10 | 10/10 | 10/10 |
| shake_bottle_horizontally | 5/10 | 5/10 | 5/10 | 10/10 | 10/10 | 10/10 |
| stack_blocks_three | 0/10 | 0/10 | 0/10 | 6/10 | 4/10 | 8/10 |
| stack_blocks_two | 0/10 | 1/10 | 0/10 | 10/10 | 8/10 | 9/10 |
| stack_bowls_three | 1/10 | 1/10 | 0/10 | 7/10 | 9/10 | 8/10 |
| stack_bowls_two | 2/10 | 7/10 | 4/10 | 10/10 | 10/10 | 9/10 |
| stamp_seal | 0/10 | 0/10 | 0/10 | 8/10 | 7/10 | 7/10 |
| turn_switch | 5/10 | 3/10 | 1/10 | 8/10 | 6/10 | 5/10 |

| **Total / 500** | **65** | **74** | **73** | **426** | **375** | **390** |
