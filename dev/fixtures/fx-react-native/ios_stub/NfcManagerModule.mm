#import <React/RCTBridgeModule.h>
#import "NfcManagerModule.swift"

@interface RtcNfcManagerBridge : NSObject <RCTBridgeModule>
@end

@implementation RtcNfcManagerBridge

RCT_EXPORT_MODULE(RtcNfcManager);

- (dispatch_queue_t)methodQueue {
  return dispatch_get_main_queue();
}

@end