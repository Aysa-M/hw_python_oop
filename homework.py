from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __str__(self) -> str:
        """
        Функция выводит на печать объект класса InfoMessage
        с помощью функции print().
        """
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.')

    def get_message(self) -> str:
        """Возвращает объект класса InfoMessage для вывода на экран."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training (ABC):
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    H_IN_MIN: ClassVar[int] = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    # Не применяется @abstractmethod, т.к. pytest выдает ошибку.
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Implemented in subclasses')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    RUN_CALORIE_1: ClassVar[float] = 18
    RUN_CALORIE_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return ((self.RUN_CALORIE_1 * self.get_mean_speed()
                - self.RUN_CALORIE_2)
                * self.weight / self.M_IN_KM * (self.duration * self.H_IN_MIN))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_CALORIE_1: ClassVar[float] = 0.035
    WALK_CALORIE_2: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        return ((self.WALK_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WALK_CALORIE_2 * self.weight)
                * (self.duration * self.H_IN_MIN))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    SWIM_CALORIE_1: ClassVar[float] = 1.1
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения плавания."""
        return (((self.length_pool * self.count_pool)
                / self.M_IN_KM) / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        return ((self.get_mean_speed() + self.SWIM_CALORIE_1)
                * 2 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Training] = {'SWM': Swimming,
                                          'RUN': Running,
                                          'WLK': SportsWalking}
    if workout_type in workout_types.keys():
        return workout_types[workout_type](*data)
    else:
        return None


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
