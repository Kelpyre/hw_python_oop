class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                traning_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float
                ) -> None:
        self.traning_type = traning_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    def info_output(self) -> str:
        output = f'Тип тренировки: {self.traning_type}; Длительность: {self.duration} ч.; ' 
        f'Дистанция: {self.distance} км; Ср. скорость: {self.speed} км/ч; Потрачено ккал: {self.calories}.'
        return output
    #pass


class Training:
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight    
        #pass

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance
        #pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed
        #pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        Message = InfoMessage()
        print(Message.info_output())
        #pass


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                action: int,
                duration: float,
                weight: float
                ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        duration_minutes = self.duration * 60
        spent_calories = (coeff_calorie_1 * self.get_mean_speed()
                          - coeff_calorie_2) * self.weight / self.M_IN_KM * duration_minutes
        return spent_calories
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    pass


class Swimming(Training):
    """Тренировка: плавание."""
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

