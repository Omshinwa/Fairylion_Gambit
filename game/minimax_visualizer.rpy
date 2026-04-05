init python:
    import json

    def minimax_load_trace(file_path="minimax_trace.json"):
        data = json.load(renpy.file(file_path))
        assert isinstance(data, _dict)
        events = data.get("events", [])
        metadata = data.get("metadata", {})
        return events, metadata

    def minimax_build_state(events, step_index):
        nodes = {}
        rows = {}
        active_node_id = None

        if not events:
            return nodes, rows, active_node_id

        end = min(step_index, len(events) - 1)

        for i in range(end + 1):
            ev = events[i]
            node_id = ev.get("node_id")
            parent_id = ev.get("parent_id")

            if node_id is None:
                continue

            if node_id not in nodes:
                nodes[node_id] = {
                    "node_id": node_id,
                    "parent_id": parent_id,
                    "children": [],
                    "move": ev.get("move"),
                    "depth": ev.get("depth", 0),
                    "alpha": ev.get("alpha"),
                    "beta": ev.get("beta"),
                    "score": ev.get("score"),
                    "event": ev.get("event"),
                    "fen": ev.get("fen"),
                    "position": ev.get("position"),
                    "maximizing": ev.get("maximizing"),
                    "ply": ev.get("ply", 0),
                    "meta": ev.get("meta", {}),
                }
            else:
                node = nodes[node_id]
                node["parent_id"] = parent_id
                node["move"] = ev.get("move", node["move"])
                node["depth"] = ev.get("depth", node["depth"])
                node["alpha"] = ev.get("alpha")
                node["beta"] = ev.get("beta")
                node["score"] = ev.get("score")
                node["event"] = ev.get("event")
                node["fen"] = ev.get("fen")
                node["position"] = ev.get("position")
                node["maximizing"] = ev.get("maximizing")
                node["ply"] = ev.get("ply", node["ply"])
                node["meta"] = ev.get("meta", {})

            if parent_id is not None and parent_id in nodes:
                if node_id not in nodes[parent_id]["children"]:
                    nodes[parent_id]["children"].append(node_id)

            active_node_id = node_id

        for node in nodes.values():
            d = node["depth"]
            if d not in rows:
                rows[d] = []
            rows[d].append(node)

        for d in rows:
            rows[d].sort(key=lambda x: x["node_id"])

        return nodes, rows, active_node_id

    def minimax_get_branch(nodes, active_node_id):
        branch = []
        cursor = active_node_id

        while cursor is not None and cursor in nodes:
            branch.append(nodes[cursor])
            cursor = nodes[cursor].get("parent_id")

        branch.reverse()
        return branch

label l_minimax_visualizer:
    call screen s_minimax_visualizer()

style style_minimax_header_text:
    size 36
    color "#111"

style style_minimax_small_text:
    size 22
    color "#222"

style style_minimax_board_text:
    font "DejaVuSansMono.ttf"
    prefer_emoji False
    size 40
    line_spacing -20
    color "#111"

screen s_minimax_visualizer(file_path="minimax_trace.json"):
    dismiss:
        action NullAction()

    default trace = minimax_load_trace(file_path)
    default events = trace[0]
    default metadata = trace[1]
    default step = 0
    $ total_steps = len(events)
    if total_steps == 0:
        add "#ddd"
        text "No minimax trace found in [file_path]" xalign 0.5 yalign 0.5 size 50 color "#111"
    else:
        $ current_step = max(0, min(step, total_steps - 1))
        $ nodes, rows, active_node_id = minimax_build_state(events, current_step)
        $ branch = minimax_get_branch(nodes, active_node_id)
        $ current_event = events[current_step]
        $ max_depth = max(rows.keys()) if rows else 0

        add "#ddd"

        vbox:
            xalign 0.5
            yalign 0.02
            spacing 8
            text "Minimax Alpha-Beta Trace Viewer" style "style_minimax_header_text"
            text "step [current_step]/[total_steps-1] | event: [current_event['event']] | node #[current_event['node_id']]" style "style_minimax_small_text"
            if metadata:
                text "best: [metadata.get('best_move')] | nodes: [metadata.get('nodes_searched')] | depth: [metadata.get('max_depth')]" style "style_minimax_small_text"

        viewport:
            draggable True
            mousewheel True
            xpos 20
            ypos 120
            xsize 1850
            ysize 770

            vbox:
                spacing 16

                frame:
                    background "#eef"
                    xfill True
                    padding (12, 12)
                    vbox:
                        text "Current Board" size 30 color "#111"
                        text current_event.get("position", "") style "style_minimax_board_text"

                frame:
                    background "#efe"
                    xfill True
                    padding (12, 12)
                    vbox:
                        text "Active Branch" size 30 color "#111"
                        if not branch:
                            text "(empty)" style "style_minimax_small_text"
                        else:
                            hbox:
                                spacing 10
                                for node in branch:
                                    frame:
                                        background ("#fbb" if node["node_id"] == active_node_id else "#fff")
                                        padding (8, 8)
                                        vbox:
                                            text "#[node['node_id']] [node.get('move') or 'ROOT']" size 22 color "#111"
                                            text "a:[node.get('alpha')] b:[node.get('beta')]" size 18 color "#333"
                                            text "s:[node.get('score')] d:[node.get('depth')]" size 18 color "#333"
                                            text "[node.get('event')]" size 18 color "#333"

                frame:
                    background "#ffe"
                    xfill True
                    padding (12, 12)
                    vbox:
                        text "Tree (visited nodes only)" size 30 color "#111"
                        for depth in range(max_depth + 1):
                            $ row_nodes = rows.get(depth, [])
                            if row_nodes:
                                hbox:
                                    spacing 10
                                    text "d[depth]:" size 24 color "#111"
                                    for node in row_nodes:
                                        $ in_branch = node in branch
                                        frame:
                                            background ("#fcc" if node["node_id"] == active_node_id else "#ddd" if in_branch else "#fff")
                                            padding (6, 6)
                                            vbox:
                                                text "#[node['node_id']] [node.get('move') or 'ROOT']" size 18 color "#111"
                                                text "a:[node.get('alpha')] b:[node.get('beta')]" size 15 color "#444"
                                                text "s:[node.get('score')]" size 15 color "#444"

        frame:
            xfill True
            yalign 1.0
            background "#ccd"
            padding (18, 14)
            hbox:
                spacing 10
                textbutton "<<" action SetScreenVariable("step", max(0, step - 50))
                textbutton "<" action SetScreenVariable("step", max(0, step - 1))
                bar:
                    value ScreenVariableValue("step", max(total_steps - 1, 1))
                    xsize 1500
                textbutton ">" action SetScreenVariable("step", min(total_steps - 1, step + 1))
                textbutton ">>" action SetScreenVariable("step", min(total_steps - 1, step + 50))

        key "K_LEFT" action SetScreenVariable("step", max(0, step - 1))
        key "K_RIGHT" action SetScreenVariable("step", min(total_steps - 1, step + 1))
