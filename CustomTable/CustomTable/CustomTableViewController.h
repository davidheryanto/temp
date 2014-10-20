//
//  CustomTableViewController.h
//  CustomTable
//
//  Created by David Heryanto on 20/10/14.
//  Copyright (c) 2014 GTT. All rights reserved.
//

#import <UIKit/UIKit.h>

#define TAG_TITLE 100
#define TAG_SUBTITLE 101
#define TAG_IMAGE 200

@interface CustomTableViewController : UITableViewController

@property (strong, nonatomic) NSMutableArray *contentArrays;

@end
