import React from 'react';
import { FlatList, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

import { useAppDispatch, useAppSelector } from '@app/store/hooks';
import { setFilter, setSort, nextPage } from '@app/store/slices/historySlice';
import type { Payment } from '@app/store/slices/paymentsSlice';

export function HistoryScreen() {
  const dispatch = useAppDispatch();
  const items = useAppSelector((s) => s.history.items);
  const filter = useAppSelector((s) => s.history.filter);
  const sort = useAppSelector((s) => s.history.sort);
  const page = useAppSelector((s) => s.history.page);
  const pageSize = useAppSelector((s) => s.history.pageSize);

  const filtered = React.useMemo(() => {
    const q = filter.toLowerCase();
    return items.filter((p) =>
      !q || p.orderId.toLowerCase().includes(q) || p.tagId.toLowerCase().includes(q),
    );
  }, [items, filter]);

  const sorted = React.useMemo(() => {
    const arr = [...filtered];
    if (sort === 'recent') arr.sort((a, b) => b.timestamp - a.timestamp);
    if (sort === 'oldest') arr.sort((a, b) => a.timestamp - b.timestamp);
    if (sort === 'amount') arr.sort((a, b) => b.amount - a.amount);
    return arr;
  }, [filtered, sort]);

  const paged = sorted.slice(0, (page + 1) * pageSize);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Historial</Text>
      <TextInput
        placeholder="Buscar por orderId o tagId..."
        value={filter}
        onChangeText={(v) => dispatch(setFilter(v))}
        style={styles.input}
      />
      <View style={styles.row}>
        {(['recent', 'oldest', 'amount'] as const).map((s) => (
          <TouchableOpacity
            key={s}
            onPress={() => dispatch(setSort(s))}
            style={[styles.chip, sort === s && styles.chipActive]}
          >
            <Text style={[styles.chipText, sort === s && styles.chipTextActive]}>
              {s === 'recent' ? 'Mas recientes' : s === 'oldest' ? 'Mas antiguos' : 'Monto'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      {paged.length === 0 ? (
        <Text style={styles.empty}>Aun no hay pagos</Text>
      ) : (
        <FlatList
          data={paged}
          keyExtractor={(p: Payment) => p.id}
          renderItem={({ item }) => (
            <View style={styles.item}>
              <Text>#{item.orderId}</Text>
              <Text>{item.amount} {item.currency} ({item.status})</Text>
            </View>
          )}
          onEndReached={() => dispatch(nextPage())}
          onEndReachedThreshold={0.5}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 12 },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 8, borderRadius: 6, marginBottom: 12 },
  row: { flexDirection: 'row', marginBottom: 12, gap: 6 },
  chip: { paddingHorizontal: 12, paddingVertical: 6, borderRadius: 16, backgroundColor: '#eee' },
  chipActive: { backgroundColor: '#6750A4' },
  chipText: { color: '#333' },
  chipTextActive: { color: '#fff' },
  empty: { color: '#888', textAlign: 'center', marginTop: 32 },
  item: { paddingVertical: 8, borderBottomWidth: 1, borderColor: '#eee' },
});