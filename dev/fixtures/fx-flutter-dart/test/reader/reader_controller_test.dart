import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:fxdart/features/reader/application/reader_controller.dart';
import 'package:fxdart/features/reader/data/document_remote_source.dart';
import 'package:fxdart/features/reader/domain/document.dart';
import 'package:fxdart/platform/native_method_channel.dart';

class _FakeChannel extends NativeMethodChannel {
  _FakeChannel(this.response) : super(channelName: 'test');
  final dynamic response;

  @override
  Future<dynamic> invoke(String method, [Object? arguments]) async {
    return response;
  }
}

void main() {
  group('ReaderController', () {
    test('returns Document when channel returns map', () async {
      final container = ProviderContainer(
        overrides: [
          documentRemoteSourceProvider.overrideWithValue(
            DocumentRemoteSource(
              channel: _FakeChannel({
                'hash': 'fxd-1',
                'title': 'Doc 1',
                'body': 'Body 1',
                'source': 'native',
              }),
            ),
          ),
        ],
      );
      addTearDown(container.dispose);
      final doc = await container.read(readerControllerProvider.future);
      expect(doc, isA<Document>());
      expect(doc!.title, 'Doc 1');
    });

    test('returns null when channel returns null', () async {
      final container = ProviderContainer(
        overrides: [
          documentRemoteSourceProvider.overrideWithValue(
            DocumentRemoteSource(channel: _FakeChannel(null)),
          ),
        ],
      );
      addTearDown(container.dispose);
      final doc = await container.read(readerControllerProvider.future);
      expect(doc, isNull);
    });
  });
}