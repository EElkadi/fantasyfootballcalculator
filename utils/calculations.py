def calculate_offensive_td_points(yards):
    if yards < 10:
        return 6
    else:
        return 6 + (yards // 10)  # 6 plus the tens digit


def calculate_qb_rushing_td_points(yards):
    if yards >= 90:
        return 25
    elif yards >= 80:
        return 20
    elif yards >= 70:
        return 18
    elif yards >= 60:
        return 16
    elif yards >= 50:
        return 14
    elif yards >= 40:
        return 12
    elif yards >= 30:
        return 10
    elif yards >= 20:
        return 8
    elif yards >= 10:
        return 7
    else:
        return 6


def calculate_qb_passing_yards_points(yards):
    if yards < 200:
        return 0
    points = 6  # Start with 6 points for 200-249 yards
    additional_yards = yards - 200
    points += additional_yards // 25  # Add 1 point for every 25 yards over 200
    return points


def calculate_qb_interceptions_points(ints):
    if ints == 0:
        return 3
    elif ints == 1:
        return 0
    else:
        return -1 * (ints - 1)


def calculate_performance_points(yards):
    return yards // 10


def calculate_points(form_data):
    player_type = form_data["player_type"]
    points = 0

    if player_type in ["QB", "RB", "WR"]:
        passing_tds = int(form_data["passing_tds"])
        passing_yards = int(form_data["passing_yards"])
        rushing_tds = int(form_data["rushing_tds"])
        rushing_yards = int(form_data["rushing_yards"])
        receiving_tds = int(form_data["receiving_tds"])
        receiving_yards = int(form_data["receiving_yards"])
        passing_two_point_conversions = int(form_data["passing_two_point_conversions"])
        rushing_two_point_conversions = int(form_data["rushing_two_point_conversions"])
        fumble_recovery_tds = int(form_data["fumble_recovery_tds"])
        interceptions = int(form_data["interceptions"])

        # Passing yards
        points += calculate_qb_passing_yards_points(passing_yards)

        # Rushing and Receiving yards
        points += calculate_performance_points(rushing_yards + receiving_yards)

        # Touchdowns
        passing_td_yards = form_data.getlist("passing_td_yards")
        for yards in passing_td_yards:
            if yards:
                points += calculate_offensive_td_points(int(yards))

        rushing_td_yards = form_data.getlist("rushing_td_yards")
        for yards in rushing_td_yards:
            if yards:
                if player_type == "QB":
                    points += calculate_qb_rushing_td_points(int(yards))
                else:
                    points += calculate_offensive_td_points(int(yards))

        receiving_td_yards = form_data.getlist("receiving_td_yards")
        for yards in receiving_td_yards:
            if yards:
                points += calculate_offensive_td_points(int(yards))

        # 2-point conversions
        points += passing_two_point_conversions * 2
        points += rushing_two_point_conversions * 3

        # Fumble recovery TDs
        points += fumble_recovery_tds * 6

        # Interceptions (negative points)
        points += calculate_qb_interceptions_points(interceptions)

    elif player_type == "K":
        field_goals = [int(fg) for fg in form_data.getlist("field_goals") if fg]
        for fg in field_goals:
            if fg >= 50:
                points += 6
            elif fg >= 30:
                points += 3
            else:
                points += 1

        game_winning_fg = form_data.get("game_winning_fg")
        if game_winning_fg == "yes":
            points += 6

    elif player_type == "DEF":
        touchdowns = int(form_data["touchdowns"])
        safeties = int(form_data["safeties"])
        sacks = int(form_data["sacks"])
        turnovers = int(form_data["turnovers"])
        points_allowed = int(form_data["points_allowed"])

        # Defensive touchdowns
        td_yards = form_data.getlist("def_td_yards")
        for yards in td_yards:
            if yards:
                points += calculate_offensive_td_points(int(yards))

        # Other defensive points
        points += safeties * 5
        points += sacks * 2
        points += turnovers * 3

        # Points allowed
        if points_allowed == 0:
            points += 10
        elif points_allowed <= 3:
            points += 7
        elif points_allowed <= 10:
            points += 3
        elif points_allowed <= 34:
            points += 0
        elif points_allowed <= 41:
            points -= 3
        elif points_allowed <= 48:
            points -= 5
        else:
            points -= 10

    return points
