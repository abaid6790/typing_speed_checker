def get_achievement(wpm):

    if wpm >= 100:
        return "🚀 Speed Demon"

    elif wpm >= 80:
        return "🥇 Fast Typist"

    elif wpm >= 60:
        return "🥈 Intermediate Typist"

    elif wpm >= 40:
        return "🥉 Beginner Typist"

    else:
        return "⌨ Keep Practicing"