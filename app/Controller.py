import pandas as pd
from io import StringIO, BytesIO
import asyncio

class AsyncCSVProcessor:
    def __init__(self, x: int, y: int, i: int, j: int):
        self.x = x  # volume average window
        self.y = y  # forward return window
        self.i = i  # bin size for volume diff
        self.j = j  # bin size for price return

    async def read_csv(self, file_bytes: bytes) -> pd.DataFrame:
        decoded = file_bytes.decode('utf-8')
        df = pd.read_csv(StringIO(decoded))
        return df

    async def process(self, file_bytes: bytes) -> BytesIO:
        df = await self.read_csv(file_bytes)

        # Clean and sort
        df = df[df['Volume'] != 0].copy()
        df['time'] = pd.to_datetime(df['time'], dayfirst=True)
        df.sort_values(by='time', inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Volume average & % difference
        vol_avg_col = f'Volume_{self.x}_day_avg'
        vol_pct_col = f'Volume_vs_{self.x}_day_avg_%'
        df[vol_avg_col] = df['Volume'].rolling(window=self.x).mean().shift(1)
        df[vol_pct_col] = ((df['Volume'] - df[vol_avg_col]) / df[vol_avg_col]) * 100

        # Price forward return
        price_ret_col = f'Price_{self.y}_day_forward_return_%'
        df[price_ret_col] = ((df['Price'].shift(-self.y) - df['Price']) / df['Price']) * 100

        # Binning
        def get_range_label(val, interval):
            if pd.isna(val):
                return None
            lower = (val // interval) * interval
            upper = lower + interval
            return f"{int(lower)} to {int(upper)}"

        vol_range_col = f'{vol_pct_col}_Range_{self.i}'
        price_range_col = f'{price_ret_col}_Range_{self.j}'
        df[vol_range_col] = df[vol_pct_col].apply(lambda v: get_range_label(v, self.i))
        df[price_range_col] = df[price_ret_col].apply(lambda v: get_range_label(v, self.j))

        # Reorder
        df = df[['time', 'Volume', vol_avg_col, vol_pct_col, vol_range_col,
                 'Price', price_ret_col, price_range_col]]

        # Crosstab
        freq_table = pd.crosstab(df[vol_range_col], df[price_range_col])

        def extract_lower_bound(label):
            try:
                return int(str(label).split(" to ")[0])
            except:
                return float('inf')

        freq_table = freq_table.reindex(sorted(freq_table.index, key=extract_lower_bound))
        freq_table = freq_table[sorted(freq_table.columns, key=extract_lower_bound)]
        df = pd.DataFrame(freq_table)
        print(df.to_numpy)

        # Save to in-memory Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            freq_table.to_excel(writer, sheet_name='Frequency_Table')
        output.seek(0)
        return output
