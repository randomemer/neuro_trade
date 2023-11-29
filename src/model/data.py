import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class StockDataset(Dataset):
    def __init__(self, data, seq_length):
        self.data = data
        self.seq_length = seq_length

    def __len__(self):
        return len(self.data) - self.seq_length

    def __getitem__(self, i):
        return self.data[i : i + self.seq_length], self.data[i + self.seq_length]


def prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    df.dropna(inplace=True)

    return df


def create_dataloaders(
    data: pd.DataFrame, seq_length: int, batch_size: int, test_size: float
):
    df = prepare_df(data)
    columns = ["open", "high", "low", "close", "volume"]
    print("Cols", columns)

    # Normalize data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(df[columns])
    normalized_df = pd.DataFrame(normalized_data, columns=columns)

    split = int(len(data) * (1 - test_size))

    train_data = normalized_df.loc[0 : split - 1].to_numpy()
    test_data = normalized_df.loc[split:].to_numpy()

    train_dataset = StockDataset(train_data, seq_length)
    test_dataset = StockDataset(test_data, seq_length)

    train_dataloader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        pin_memory=True,
    )

    test_dataloader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=True,
        pin_memory=True,
    )

    return train_dataloader, test_dataloader
