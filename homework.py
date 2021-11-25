class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def show_training_info(self) -> None:
        """Создает объект класса InfoMessage."""
        print(f'Тип тренировки: {self.training_type};'
              f'Длительность: {self.duration} ч.;'
              f'Дистанция: {self.distance} км;'
              f'Ср. скорость: {self.speed} км/ч;'
              f'Потрачено ккал: {self.calories}.')

    def __str__(self) -> None:
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
        """Возвращает объект класса InfoMessage для дальнейшей работы с ним."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


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

    def get_distance(self, ) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed = (Training.get_distance(self) / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        run_calorie_1: float = 18
        run_calorie_2: float = 20
        self.calories = ((run_calorie_1 * Training.get_mean_speed(self)
                         - run_calorie_2)
                         * self.weight / self.M_IN_KM * (self.duration * 60))
        return self.calories


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
        """Получить количество затраченных калорий при спортивной ходьбе."""
        walk_calorie_1: float = 0.035
        walk_calorie_2: float = 0.029
        self.calories = ((walk_calorie_1 * self.weight
                         + (Training.get_mean_speed(self) ** 2 // self.height)
                         * walk_calorie_2 * self.weight)
                         * (self.duration * 60))
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения плавания."""
        self.speed = (((self.length_pool * self.count_pool)
                      / self.M_IN_KM) / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        swim_calorie_1: float = 1.1
        self.calories = ((Swimming.get_mean_speed(self) + swim_calorie_1)
                         * 2 * self.weight)
        return self.calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type in workout_types.keys():
        return workout_types[workout_type](*data)
    else:
        return 'No such a type of training.'


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
