import { useAppDispatch } from '@app/store/hooks';
import { addPayment, markPendingSync, setProcessing, setLastError } from '@app/store/slices/paymentsSlice';
import type { Payment } from '@app/store/slices/paymentsSlice';
import { NfcManager } from '@features/payments/data/NfcManager';

export class PaymentsController {
  constructor(private dispatch: ReturnType<typeof useAppDispatch>) {}

  async startProcessing(orderId: string, amount: number, currency = 'USD'): Promise<void> {
    this.dispatch(setProcessing(true));
    this.dispatch(setLastError(undefined));
    try {
      await NfcManager.start();
      const tag = await NfcManager.readTag();
      if (!tag) {
        this.dispatch(setLastError('Tag no reconocido'));
        return;
      }
      const payment: Payment = {
        id: `pay-${Date.now()}`,
        orderId,
        amount,
        currency,
        tagId: tag.tagId,
        status: 'success',
        timestamp: Date.now(),
      };
      this.dispatch(addPayment(payment));
    } catch (err: any) {
      this.dispatch(setLastError(err?.message ?? 'NFC error'));
      this.dispatch(
        addPayment({
          id: `pay-${Date.now()}`,
          orderId,
          amount,
          currency,
          tagId: 'unknown',
          status: 'error',
          timestamp: Date.now(),
        })
      );
      this.dispatch(markPendingSync(orderId));
    } finally {
      this.dispatch(setProcessing(false));
    }
  }
}