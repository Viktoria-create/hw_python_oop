class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_tupe, duration, distance, speed, calories):
        self.training_type = training_tupe
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f"Тип тренировки: {self.training_type};"
            f"Длительность: {self.duration: 3.3 f} ч.;"
            f"Дистанция: {self.distance: 3.3 f} км;"
            f"Ср. скорость: {self.speed: 3.3 f} км/ч;"
            f"Потрачено ккал: {self.calories: 3.3 f}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        # Метод возвращает дистанцию.
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # Метод возвращает преодоленную дистанцию.
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        show_message = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return show_message


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        self.coeff_calories_1: int = 18
        self.coeff_calories_2: int = 20
        time_in_minuts = self.duration * 60
        return (
            self.coeff_calories_1 * self.get_mean_speed()
            - self.coeff_calories_2
            * (self.weight / self.M_IN_KM * time_in_minuts))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.weight = weight
        self.height = height
        self.duration = duration * 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченых каллорий."""
        self.coeff_calories_1: float = 0.035
        self.coeff_calories_2: float = 0.029
        self.coeff_calories_3: float = 2
        calories_in_walking = ((self.coeff_calories_1 * self.weight
                                + (self.get_mean_speed() ** 2 // self.height)
                                * self.coeff_calories_2
                                * self.weight)) * self.duration
        return calories_in_walking


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        lenght_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        self.coeff_calorie_1: float = 1.1
        self.coeff_calorie_2: float = 2
        return (
            (self.get_mean_speed() + self.coeff_calorie_1)
            * self.coeff_calorie_2
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())

    if __name__ == "__main__":
        packages = [
            ("SWM", [720, 1, 80, 25, 40]),
            ("RUN", [15000, 1, 75]),
            ("WLK", [9000, 1, 75, 180]),
        ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
