"""Модуль фитнес-трекера"""

from dataclasses import dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    # pytest обязывает иметь переменную duration в InfoMessage
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    OUTPUT_MSG: str = (
        'Тип тренировки: {}; '
        'Длительность: {} ч.; '
        'Дистанция: {} км; '
        'Ср. скорость: {} км/ч; '
        'Потрачено ккал: {}'
    )

    def get_message(self) -> str:
        """Вывести информационное сообщение"""
        output: str = self.OUTPUT_MSG.format(
            f'{self.training_type}',
            f'{self.duration:.3f}',
            f'{self.distance:.3f}',
            f'{self.speed:.3f}',
            f'{self.calories:.3f}.'
        )
        return output


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: int = 60
    IMP_ERR_MSG: str = ('Метод {} не имплементирован в дочерний класс {}!')

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        self.action: int = action
        self.duration_hours: float = duration
        self.weight: float = weight
        self.duration_minutes: float = self.duration_hours * self.MIN_IN_HOUR

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration_hours
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(self.IMP_ERR_MSG.format(
            'self.get_spent_calories()', f'{type(self).__name__}'
        )
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message: InfoMessage = InfoMessage(
            self.__class__.__name__,
            self.duration_hours,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return message


class Running(Training):
    """Тренировка: бег."""

    RUN_CALORIE_C1: float = 18
    RUN_CALORIE_C2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = (
            ((self.RUN_CALORIE_C1 * self.get_mean_speed())
             - self.RUN_CALORIE_C2) * self.weight
            / self.M_IN_KM * self.duration_minutes
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WLK_CALORIE_C1: float = 0.035
    WLK_CALORIE_C2: float = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float
    ) -> None:
        super().__init__(
            action,
            duration,
            weight
        )
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = (
            (self.WLK_CALORIE_C1 * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.WLK_CALORIE_C2 * self.weight)
            * self.duration_minutes
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SWM_CALORIE_C1: float = 1.1
    SWM_CALORIE_C2: float = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float
    ) -> None:
        super().__init__(
            action,
            duration,
            weight
        )
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration_hours
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = (
            (self.get_mean_speed() + self.SWM_CALORIE_C1)
            * (self.SWM_CALORIE_C2 * self.weight)
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    VALUE_ERR_MSG: str = 'Неизвестный тип тренировки!'

    dict_class: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in dict_class:
        object_class: Training = dict_class[workout_type](*data)
        return object_class
    raise ValueError(VALUE_ERR_MSG)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    info_to_print: str = info.get_message()
    print(info_to_print)


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
