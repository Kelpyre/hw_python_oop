class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                training_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float
                ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    def get_message(self) -> str:
        output = (f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; '
                  f'Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}.')
        return output
    #pass


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight    
        self.duration_minutes = self.duration * 60
        #pass

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
        Message = InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())
        return Message
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
        spent_calories = ((coeff_calorie_1 * self.get_mean_speed()
                          - coeff_calorie_2) * self.weight / self.M_IN_KM * self.duration_minutes)
        return spent_calories
    #pass

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                height: float
                ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        spent_calories = ((coeff_calorie_1 * self.weight
                          + (self.get_mean_speed() ** 2 // self.height)
                          * coeff_calorie_2 * self.weight) * self.duration_minutes)
        return spent_calories
    #pass


class Swimming(Training):

    LEN_STEP = 1.38

    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                length_pool: float,
                count_pool: float
                ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Тренировка: плавание."""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        spent_calories = ((self.get_mean_speed() + coeff_calorie_1)
                        * (coeff_calorie_2 * self.weight))
        return spent_calories
    #pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict = {'SWM' : Swimming, 'RUN' : Running, 'WLK' : SportsWalking}
    for key_word in dict:
        if key_word is workout_type:
            Object = dict[key_word](*data)
        else:
            pass
    return Object
    #pass


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info_to_print = info.get_message()
    print(info_to_print)
    #pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

