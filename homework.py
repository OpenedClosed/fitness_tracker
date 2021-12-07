"""Программа для работы фитнес-трекера."""
import sys
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info_message = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        """Сообщение о тренировке."""
        info_ = self.info_message.format(training_type=self.training_type,
                                         duration=self.duration,
                                         distance=self.distance,
                                         speed=self.speed,
                                         calories=self.calories
                                         )
        return info_


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist_in_km = self.action * self.LEN_STEP / self.M_IN_KM
        return dist_in_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_spead = self.get_distance() / self.duration_h
        return mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        information = InfoMessage(type(self).__name__,
                                  self.duration_h,
                                  self.get_distance(),
                                  self.get_mean_speed(),
                                  self.get_spent_calories()
                                  )
        return information


class Running(Training):
    """Тренировка: бег."""

    COEFF_CAL_1: int = 18
    COEFF_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        dur_in_min: float = self.duration_h * self.H_IN_MIN
        calories: float = ((self.COEFF_CAL_1 * self.get_mean_speed()
                           - self.COEFF_CAL_2)
                           * self.weight / self.M_IN_KM * dur_in_min)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CAL_1: float = 0.035
    COEFF_CAL_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        dur_in_min: float = self.duration_h * self.H_IN_MIN
        calories: float = ((self.COEFF_CAL_1 * self.weight
                           + (self.get_mean_speed()**2 // self.height)
                           * self.COEFF_CAL_2 * self.weight) * dur_in_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CAL_1: float = 1.1
    COEFF_CAL_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_spead = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration_h)
        return mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.get_mean_speed() + self.COEFF_CAL_1)
                           * self.COEFF_CAL_2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    conform: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    exc_message: str = 'Ошибка'

    if workout_type in conform:
        exercise: Training = conform[workout_type](*data)
        return exercise
    else:
        print(exc_message)
        sys.exit()


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

    for workout_type_, data_ in packages:
        training_ = read_package(workout_type_, data_)
        main(training_)
